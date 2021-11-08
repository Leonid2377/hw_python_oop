from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training};'
               ' Длительность: {duration:.3f} ч.;'
               ' Дистанция: {distance:.3f} км;'
               ' Ср. скорость: {speed:.3f} км/ч;'
               ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        message_list = {'training': self.training_type,
                        'duration': self.duration,
                        'distance': self.distance,
                        'speed': self.speed,
                        'calories': self.calories
                        }
        return self.MESSAGE.format(**message_list)


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # Расстояние, которое спортсмен преодолевает за один шаг
    M_IN_KM = 1000  # Константа для перевода значений из метров в километры.
    MIN_IN_HR = 60  # Коеффицент расчета часов в минуты
    COEFFICIENT_SPEED_1 = 18  # Коеффицент расчета для класса Running
    COEFFICIENT_SPEED_2 = 20  # Коеффицент расчета для класса Running
    COEFFICIENT_WEIGHT_1 = 0.035  # Коеффицент расчета для класса SportsWalking
    COEFFICIENT_WEIGHT_2 = 0.029  # Коеффицент расчета для класса SportsWalking
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
            type(self).__name__,  # self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    action: int
    duration: float
    weight: float

    def get_spent_calories(self) -> float:
        return ((self.COEFFICIENT_SPEED_1 * self.get_mean_speed()
                - self.COEFFICIENT_SPEED_2) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HR))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        return ((self.COEFFICIENT_WEIGHT_1 * self.weight
                 + (self.get_mean_speed()**2 // self.height)
                 * self.COEFFICIENT_WEIGHT_2 * self.weight)
                * self.duration * self.MIN_IN_HR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFFICIENT_SPEED_1 = 1.1
    COEFFICIENT_SPEED_2 = 2
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.COEFFICIENT_SPEED_1)
                * self.COEFFICIENT_SPEED_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        dict_training = {'SWM': Swimming,
                         'RUN': Running,
                         'WLK': SportsWalking}
        return dict_training[workout_type](*data)
    # except Exception as e:
    except KeyError as key:
        print(f'Ошибка входных данных! '
              f'Несоотвтетствующий вид данных, тип тренировки {key} ')
        raise
    except TypeError:
        print('Ошибка! дано неверное кол-во аргументов')
        raise


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
        main(read_package(workout_type, data))
