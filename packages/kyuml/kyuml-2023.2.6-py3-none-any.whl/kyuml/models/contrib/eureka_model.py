from typing import Any, Dict, List, Union

import numpy as np
from pandas import DataFrame
from pytz import timezone
import torch

from kyuml.models import AutogluonTrainableCustom

TZ = timezone("Asia/Seoul")

class EurekaModel(AutogluonTrainableCustom):
    def __init__(
        self,
        model_name: str,
        model_version: str,
        features: List[str],
        model=None,
        predict_fn: str = "predict",
        data: Dict[str, Any] = {},
    ):
        assert isinstance(features, list), "`features`은 list 타입이어야 합니다."

        assert isinstance(predict_fn, str), "`predict_fn`은 str 타입이어야 합니다."
        assert predict_fn in [
            "predict",
            "predict_proba",
            "none",
        ], "`predict_fn`은 predict, predict_proba, none 중 하나의 값이어야 합니다."

        assert isinstance(data, dict), "`data`는 dict 타입이어야 합니다."

        super().__init__([model], model_name, model_version, features)

        self.preprocess_logic = preprocess_logic
        self.predict_fn = predict_fn
        self.data = data

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        preprocessed_x = self._preprocess(x, kwargs.get("keys", []))
        y = self._ml_predict(preprocessed_x)
        items = self._postprocess(x, kwargs.get("keys", []), y) or []

        return {"items": items}

    def _preprocess(
        self,
        x: List[Any],
        additional_keys: List[Any]
    ) -> List[Any]:
        assert len(self.features) == len(x), "`x`의 길이가 `features`의 길이와 다릅니다."

        data = {name: x[i] for i, name in enumerate(self.features) if x[i] not in [None, []]}
        data["additional_keys"] = additional_keys
        data.update(self.data)

    def _ml_predict(self, preprocessed_x: List[Any]) -> Union[float, List[float], str, None]:
        try:
            if self.predict_fn == "none" and self.model_lib != "pytorch":
                return None

            if not isinstance(preprocessed_x[0], list):
                preprocessed_x = [preprocessed_x]

            if self.model_lib == "autogluon":
                input_data = DataFrame(
                    preprocessed_x, columns=[f for f in self.features if f not in self.non_training_features]
                )
            elif self.model_lib == "pytorch":
                input_data = torch.tensor(preprocessed_x, dtype=torch.float)
            else:
                input_data = np.array(preprocessed_x)

            if self.model_lib == "pytorch":
                y = self.models[0](input_data).detach().numpy()
            elif self.predict_fn == "predict":
                y = self.models[0].predict(input_data)
            else:
                y = self.models[0].predict_proba(input_data)
                if self.model_lib == "autogluon" and isinstance(y, DataFrame):
                    y = y.to_numpy()

            if len(y) == 1:
                y = y[0]

            try:
                return y.tolist()
            except AttributeError:
                return y

        except Exception as e:
            raise Exception(f"EurekaModel: ML Prediction에 실패했습니다. {e}")

    def _postprocess(
        self,
        x: List[Any],
        additional_keys: List[Any],
        y: Union[float, List[float], None],
    ) -> List[Dict[str, Any]]:

        data = {name: x[i] for i, name in enumerate(self.features) if x[i] not in [None, []]}
        data["additional_keys"] = additional_keys
        data["y"] = y
        data.update(self.data)
        
        return data