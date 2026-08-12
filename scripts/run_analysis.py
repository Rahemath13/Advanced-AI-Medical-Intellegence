import argparse

from app.services.prediction_service import (
    PredictionService,
)


def main() -> None:
    """Run complete medical image analysis."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image",
        required=True,
        help="Path to chest X-ray image.",
    )

    args = parser.parse_args()

    service = PredictionService()

    result = service.analyze(args.image)

    print("=" * 60)
    print("ADVANCED AI MEDICAL ANALYSIS")
    print("=" * 60)

    print(f"Prediction: {result['prediction']}")

    print(f"Confidence: {result['confidence']:.4f}")

    print(f"Normal probability: {result['normal_probability']:.4f}")

    print(f"Pneumonia probability: {result['pneumonia_probability']:.4f}")

    print(f"Grad-CAM: {result['xai_path']}")

    print("\nAI-ASSISTED REPORT")
    print("-" * 60)

    report = result["report"]

    print(f"\nSummary:\n{report['summary']}")

    print("\nFindings:")

    for finding in report["findings"]:
        print(f"- {finding}")

    print(f"\nImpression:\n{report['impression']}")

    print("\nRecommendations:")

    for recommendation in report["recommendations"]:
        print(f"- {recommendation}")

    print(f"\nDisclaimer:\n{report['disclaimer']}")


if __name__ == "__main__":
    main()
