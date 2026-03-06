from orchestrator import Orchestrator
from config import SAMPLES_CSV, OUTPUT_CSV


def main():
    """Entry point for the Multi-Agent Bug Detection System."""
    print("Initializing Multi-Agent Pipeline...")
    
    pipeline = Orchestrator()
    pipeline.process_dataset(input_csv=SAMPLES_CSV, output_csv=OUTPUT_CSV)


if __name__ == "__main__":
    main()
