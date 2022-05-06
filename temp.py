from typing import Sequence, Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
        self, training_type: str, duration: float, distance: float,
            speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Формирует сообщение о результатах."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MINUTES_IN_HOUR: float = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance()/self.duration

    def get_spent_calories(self) -> float:
        """Получить количество потраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__, self.duration,
            self.get_distance(), self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        """Расчет калорий бега."""
        return ((
            self.COEFF_CALORIE_1 * self.get_mean_speed() -
            self.COEFF_CALORIE_2)
            * self.weight / super().M_IN_KM * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 2
    COEFF_CALORIE_3: float = 0.029

    def __init__(
        self, action: int,
        weight: float,
        height: float,
        duration: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет калорий ходьбы."""
        return (
            (self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed()**self.COEFF_CALORIE_2
                    // self.height)
                * self.COEFF_CALORIE_3 * self.weight) * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    def __init__(
        self, action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию по плаванью."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Средняя скорость плаванья."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Расчет калорий плаванья."""
        return (
            (self.get_mean_speed() + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2 * self.weight)


def read_package(
    workout_type: str, data: Sequence[Union[int, str]]
) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dic = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
        }
    return workout_dic[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    return print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]), ]

for workout_type, data in packages:
    training = read_package(workout_type, data)
    main(training)
