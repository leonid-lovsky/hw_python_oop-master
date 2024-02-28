from dataclasses import dataclass
from typing import Any, Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получить сообщение о выполненной тренировке."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65

    M_IN_KM: int = 1000
    M_IN_HOUR: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_in_meters = self.action * self.LEN_STEP
        return distance_in_meters / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        return InfoMessage(
            training_type, duration, distance, mean_speed, spent_calories
        )


class Running(Training):
    """Тренировка: бег."""

    CAL_SPEED_FACTOR: float = 18
    CAL_SPEED_SHIFT: float = 20

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        weight = self.weight
        duration_in_minutes = self.duration * self.M_IN_HOUR
        return (
            (self.CAL_SPEED_FACTOR * mean_speed - self.CAL_SPEED_SHIFT)
            * weight / self.M_IN_KM * duration_in_minutes
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CAL_WEIGHT_FACTOR: float = 0.035
    CAL_SPEED_POWER: float = 2
    CAL_SPEED_FACTOR: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        weight = self.weight
        height = self.height
        duration_in_minutes = self.duration * self.M_IN_HOUR
        return (
            (
                self.CAL_WEIGHT_FACTOR * weight
                + (mean_speed**self.CAL_SPEED_POWER // height)
                * self.CAL_SPEED_FACTOR * weight
            ) * duration_in_minutes
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    CAL_SPEED_SHIFT: float = 1.1
    CAL_SPEED_FACTOR: float = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return (
            (mean_speed + self.CAL_SPEED_SHIFT)
            * self.CAL_SPEED_FACTOR * self.weight
        )


WORKOUT_TYPE: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: List[Any]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in WORKOUT_TYPE:
        message = f'Не допустимое значение workout_type: {workout_type}'
        raise ValueError(message)

    return WORKOUT_TYPE[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
