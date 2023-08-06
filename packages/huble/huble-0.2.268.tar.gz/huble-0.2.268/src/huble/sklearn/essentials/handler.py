class EssentialsHandler:
    def __init__(self) -> None:
        pass

    def return_function(self, function_name: str, params: dict, task_type: str):

        essentials = {
            "Train-Test Split": self.__train_test_split,
            "Train Model": self.__train_model,
        }
        return essentials[function_name](params, task_type)

    def __train_test_split(self, params, task_type):
        parameters = {
            "test_size": params["test_size"],
        }
        return f"training_dataset, test_dataset = huble.sklearn.train_test_split(data=data,parameters={parameters})"

    def __train_model(self, params, task_type):
        return f"Model, input_format, filename = huble.sklearn.train_model(data=training_dataset, model=model, column='{params['target_column']}', task_type='{task_type}')"
