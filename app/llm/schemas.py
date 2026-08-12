from pydantic import BaseModel, Field


class MedicalReportRequest(BaseModel):
    prediction: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    normal_probability: float = Field(
        ge=0.0,
        le=1.0,
    )
    pneumonia_probability: float = Field(
        ge=0.0,
        le=1.0,
    )


class MedicalReport(BaseModel):
    summary: str
    findings: list[str]
    impression: str
    recommendations: list[str]
    disclaimer: str
