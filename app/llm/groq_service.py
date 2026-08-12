import json
import re

from groq import Groq

from app.core.config import get_settings
from app.llm.schemas import MedicalReport, MedicalReportRequest


class GroqMedicalReportService:
    """Generate structured medical decision-support reports using Groq with rule-based fallback."""

    def __init__(self) -> None:
        settings = get_settings()

        self.client = None
        self.model = settings.groq_model

        if settings.groq_api_key and not settings.groq_api_key.startswith("your_"):
            try:
                self.client = Groq(
                    api_key=settings.groq_api_key,
                )
            except Exception:
                self.client = None

    @staticmethod
    def _clean_json_response(content: str) -> str:
        """Remove markdown code fences and extract the JSON object."""

        content = content.strip()

        content = re.sub(
            r"^```(?:json)?\s*",
            "",
            content,
            flags=re.IGNORECASE,
        )

        content = re.sub(
            r"\s*```$",
            "",
            content,
        )

        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError(
                "Groq response did not contain a valid JSON object."
            )

        return content[start : end + 1]

    @staticmethod
    def _validate_report(data: dict) -> MedicalReport:
        """Validate Groq output against the application schema."""

        return MedicalReport.model_validate(data)

    def _generate_fallback_report(
        self,
        request: MedicalReportRequest,
    ) -> MedicalReport:
        """Generate a rule-based medical decision support report when LLM is unavailable."""

        is_pneumonia = request.prediction.upper() == "PNEUMONIA"

        if is_pneumonia:
            summary = (
                f"Deep learning analysis indicates findings consistent with Pneumonia "
                f"(Confidence: {request.confidence * 100:.1f}%)."
            )
            impression = (
                f"Pulmonary opacity features detected with "
                f"{request.pneumonia_probability * 100:.1f}% model probability."
            )
            findings = [
                f"EfficientNet-B0 Pneumonia probability: {request.pneumonia_probability * 100:.1f}%",
                f"EfficientNet-B0 Normal probability: {request.normal_probability * 100:.1f}%",
                "Grad-CAM heatmap visualizes localized attention regions associated with potential infiltrate.",
            ]
            recommendations = [
                "Correlate findings with patient clinical symptoms (fever, cough, auscultation).",
                "Consult a licensed radiologist for formal diagnostic interpretation.",
                "Consider follow-up imaging or laboratory evaluation as clinically indicated.",
            ]
        else:
            summary = (
                f"Deep learning analysis indicates Normal chest X-ray findings "
                f"(Confidence: {request.confidence * 100:.1f}%)."
            )
            impression = (
                f"No radiographic evidence of pneumonia detected "
                f"({request.normal_probability * 100:.1f}% normal probability)."
            )
            findings = [
                f"EfficientNet-B0 Normal probability: {request.normal_probability * 100:.1f}%",
                f"EfficientNet-B0 Pneumonia probability: {request.pneumonia_probability * 100:.1f}%",
                "Grad-CAM heatmap shows non-focal attention distribution across lung fields.",
            ]
            recommendations = [
                "Maintain standard clinical monitoring as clinically warranted.",
                "Re-evaluate if respiratory symptoms develop or progress.",
            ]

        disclaimer = (
            "This decision-support report was generated automatically based on "
            "deep learning classifier probabilities. It is not a definitive medical diagnosis "
            "and requires review by a qualified healthcare professional."
        )

        return MedicalReport(
            summary=summary,
            findings=findings,
            impression=impression,
            recommendations=recommendations,
            disclaimer=disclaimer,
        )

    def generate_report(
        self,
        image_path,
        request: MedicalReportRequest,
    ) -> MedicalReport:
        """
        Generate an AI-assisted medical report.

        Falls back to rule-based generation if Groq API is unavailable or fails.
        """

        if self.client is None:
            return self._generate_fallback_report(request)

        system_prompt = """
You are an AI medical decision-support report writer.

You are NOT a doctor and must NOT claim definitive diagnosis.

Generate a concise, clinically structured chest X-ray
decision-support report from the machine-learning classification
results supplied by the application.

IMPORTANT:
- Return ONLY one valid JSON object.
- Do NOT use Markdown.
- Do NOT use ```json.
- Do NOT add text before or after the JSON.
- Every required field must be present.
- findings must be a JSON array of strings.
- recommendations must be a JSON array of strings.
- Do not invent patient history, age, symptoms, laboratory results,
  anatomical findings, pleural effusion, consolidation, or other
  radiological findings that were not provided as evidence.
- Clearly distinguish AI classification from definitive diagnosis.
- Always include an appropriate medical-review disclaimer.

Required JSON format:

{
  "summary": "string",
  "findings": ["string"],
  "impression": "string",
  "recommendations": ["string"],
  "disclaimer": "string"
}
"""

        user_prompt = f"""
Create the report using ONLY these verified model outputs:

Predicted class: {request.prediction}
Overall confidence: {request.confidence:.4f}
Normal probability: {request.normal_probability:.4f}
Pneumonia probability: {request.pneumonia_probability:.4f}

Do not claim visual radiological findings that were not supplied.
The report must describe this as AI decision-support information.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                response_format={
                    "type": "json_object",
                },
                temperature=0.1,
                max_tokens=700,
            )

            content = response.choices[0].message.content or ""

            if not content.strip():
                return self._generate_fallback_report(request)

            json_content = self._clean_json_response(content)
            data = json.loads(json_content)
            return self._validate_report(data)

        except Exception:
            return self._generate_fallback_report(request)