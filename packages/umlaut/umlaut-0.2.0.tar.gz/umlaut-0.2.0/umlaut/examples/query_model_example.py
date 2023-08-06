if __name__ == "__main__":
    """Saves the model to MLflow in an experiment run"""
    import os
    import sys

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    from umlaut import Umlaut

    result = Umlaut.query_model(
        model_name="Quarterly Revenue",
        input_config={"revenue": 3},
        stage="Staging",
    )
    print(f"Revenue will{'' if result else ' not'} exceed target")
