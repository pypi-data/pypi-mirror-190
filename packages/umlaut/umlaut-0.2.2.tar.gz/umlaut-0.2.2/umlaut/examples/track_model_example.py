class ExampleModel():
    """Example business logic that can be wrapped into a model.
       The class must contain a 'predict', 'query', or 'run' method."""
    def business_logic(self, revenue: int) -> bool:
        return revenue > 5

    def predict(self, model_input: dict) -> bool:
        return self.business_logic(revenue=model_input.get("revenue"))


if __name__ == "__main__":
    """Saves the model to MLflow in an experiment run"""
    import os
    import sys

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    from umlaut import Umlaut

    Umlaut.track_model(
        model=ExampleModel(),
        model_name="Quarterly Revenue",
        run_name="Update",
    )
