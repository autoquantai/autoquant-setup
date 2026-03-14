import pandas as pd
from sklearn.linear_model import LogisticRegression

from autoquant_cli.quant.model_base import AutoQuantModel


class SeedModel(AutoQuantModel):
    def create_features(self, frame: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
        frame = frame.copy()
        close = frame["close"]
        high = frame["high"]
        low = frame["low"]
        volume = frame["volume"]
        frame["feature_return_1"] = close.pct_change().fillna(0.0)
        frame["feature_return_6"] = close.pct_change(6).fillna(0.0)
        frame["feature_range"] = ((high - low) / close.replace(0.0, 1.0)).fillna(0.0)
        frame["feature_volume_change"] = volume.pct_change().replace([float("inf"), float("-inf")], 0.0).fillna(0.0)
        frame["feature_trend_12"] = ((close / close.rolling(12).mean()) - 1.0).replace(
            [float("inf"), float("-inf")], 0.0
        ).fillna(0.0)
        frame["target"] = (close.shift(-1) > close).astype(int)
        frame = frame.iloc[:-1].reset_index(drop=True)
        return frame, [
            "feature_return_1",
            "feature_return_6",
            "feature_range",
            "feature_volume_change",
            "feature_trend_12",
        ]

    def get_hyperparameter_candidates(self) -> dict[str, object]:
        return {
            "c": [0.1, 1.0, 10.0],
            "class_weight": ["balanced", None],
            "solver": ("lbfgs", "liblinear"),
            "max_iter": range(200, 1001, 200),
            "tol": (1e-5, 1e-2),
            "intercept_scaling": (1, 5),
            "fit_intercept": [True, False],
            "random_state": 42,
        }

    def fit(self, x_train: pd.DataFrame, y_train: pd.Series, hyperparams: dict[str, object]) -> None:
        self.model = LogisticRegression(
            C=hyperparams.get("c", 1.0),
            class_weight=hyperparams.get("class_weight"),
            solver=hyperparams.get("solver", "lbfgs"),
            max_iter=hyperparams.get("max_iter", 1000),
            tol=hyperparams.get("tol", 1e-4),
            intercept_scaling=hyperparams.get("intercept_scaling", 1.0),
            fit_intercept=hyperparams.get("fit_intercept", True),
            random_state=hyperparams.get("random_state", 42),
        )
        self.model.fit(x_train, y_train)

    def predict(self, x_test: pd.DataFrame) -> list[float | int]:
        return self.model.predict(x_test).tolist()
