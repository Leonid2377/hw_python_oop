from dataclasses import dataclass, asdict, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type};'
               ' Длительность: {duration:.3f} ч.;'
               ' Дистанция: {distance:.3f} км;'
               ' Ср. скорость: {speed:.3f} км/ч;'
               ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # Расстояние, которое спортсмен преодолевает за один шаг
    M_IN_KM = 1000  # Константа для перевода значений из метров в километры.
    MIN_IN_HR = 60  # Коеффицент расчета часов в минуты
    action: int  # количество совершённых действий
    duration: float  # длительность тренировки
    weight: float  # вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    MULTIPLIER_SPEED = 18
    SHIFT_SPEED = 20

    def get_spent_calories(self) -> float:
        return ((self.MULTIPLIER_SPEED * self.get_mean_speed()
                - self.SHIFT_SPEED) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HR))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    MULTIPLIER_WEIGHT = 0.035
    SECOND_MULTIPLIER_WEIGHT = 0.029

    def get_spent_calories(self) -> float:
        return ((self.MULTIPLIER_WEIGHT * self.weight
                 + (self.get_mean_speed()**2 // self.height)
                 * self.SECOND_MULTIPLIER_WEIGHT * self.weight)
                * self.duration * self.MIN_IN_HR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SUMMAND_SPEED = 1.1
    MULTIPLIER_SPEED = 2
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.SUMMAND_SPEED)
                * self.MULTIPLIER_SPEED
                * self.weight)


TRAININGS = {'SWM': Swimming,
             'RUN': Running,
             'WLK': SportsWalking}

ERROR_ONE = 'Выбран не верный тип тренировки: {type_training}.'
ERROR_TWO = ('Для типа тренировки {type_training},'
             ' ожидаемое кол-во значений: {expected_value},'
             ' полученное: {result_value}')


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAININGS:
        raise ValueError(ERROR_ONE.format(type_training=workout_type))

    training_unpacking = TRAININGS[workout_type]

    if len(data) != len(fields(training_unpacking)):
        raise ValueError(ERROR_TWO.format(type_training=workout_type,
                                          expected_value=len(data),
                                          result_value=len(
                                              fields(
                                                  training_unpacking))))
    return training_unpacking(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
