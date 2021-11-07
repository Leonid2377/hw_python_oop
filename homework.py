class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message_list = (f'Тип тренировки: {self.training_type};'
                        f' Длительность: {self.duration:.3f} ч.;'
                        f' Дистанция: {self.distance:.3f} км;'
                        f' Ср. скорость: {self.speed:.3f} км/ч;'
                        f' Потрачено ккал: {self.calories:.3f}.')
        return message_list


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # Расстояние, которое спортсмен преодолевает за один шаг
    M_IN_KM = 1000  # Константа для перевода значений из метров в километры.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action  # количество совершённых действий
        self.duration = duration  # длительность тренировки
        self.weight = weight  # вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = ((self.action * self.LEN_STEP) / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return message


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action, duration, weight):
        self.COEFF_CALORIE_1 = 18
        self.COEFF_CALORIE_2 = 20
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        run = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
               * (self.duration * 60))
        return run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height):
        self.COEFF_CALORIE_1 = 0.035
        self.COEFF_CALORIE_2 = 0.029
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        sports_walking = ((self.COEFF_CALORIE_1 * self.weight
                           + (self.get_mean_speed()**2 // self.height)
                           * self.COEFF_CALORIE_2 * self.weight)
                          * self.duration * 60)
        return sports_walking


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        self.length_pool = length_pool  # длина бассейна в метрах
        self.count_pool = count_pool  # кол-во раз
        # пользователь переплыл бассейн
        super().__init__(action, duration, weight)
        self.COEFF_CALORIE_1 = 1.1
        self.COEFF_CALORIE_2 = 2

    def get_mean_speed(self) -> float:
        mean_spd_swim = (self.length_pool
                         * self.count_pool
                         / self.M_IN_KM / self.duration)
        return mean_spd_swim

    def get_spent_calories(self) -> float:
        swim_calories = ((self.get_mean_speed()
                          + self.COEFF_CALORIE_1)
                         * self.COEFF_CALORIE_2
                         * self.weight)
        return swim_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(*data)
    elif workout_type == 'RUN':
        return Running(*data)
    else:
        return SportsWalking(*data)


def main(training: Training) -> None:
    """Главная функция."""
    message = training.show_training_info()
    print(message.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
