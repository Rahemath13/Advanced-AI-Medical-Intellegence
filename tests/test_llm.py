from app.llm.schemas import MedicalReportRequest


def test_medical_report_request():
    request = MedicalReportRequest(
        prediction="PNEUMONIA",
        confidence=0.9678,
        normal_probability=0.0322,
        pneumonia_probability=0.9678,
    )

    assert request.prediction == "PNEUMONIA"
    assert request.confidence == 0.9678
    assert request.pneumonia_probability == 0.9678
