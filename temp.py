from typing import Dict

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
                 self, training_type: str, 
                 duration: float, 
                 distance: float, 
                 speed: float, 
                 calories: float):
        self.training_type: str = training_type
        self.duration: float  = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calaries: float = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность тренировки {self.duration} ч; '
            f'Пройденая дистанция {self.distance} км; '
            f'Средняя скорость {self.speed} км/ч; '
            f'Потрачено каллорий {self.calaries} калл.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: float = 60
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * Training.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, 
                           self.duration,
                           self.get_distance(), 
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20
    def get_spent_calories(self) -> float:
        return (
                (self.COEFF_CALORIE_1 * self.get_mean_speed()
                 - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * self.duration * self.M_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_3: float = 0.035
    COEFF_CALORIE_4: float = 0.029

    def __init__(
                 self, action: int, 
                 duration: float,
                 weight: float, 
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        return (
                (self.COEFF_CALORIE_3 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.COEFF_CALORIE_4 * self.weight) * self.duration
                 * self.M_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_calorie_5: float = 1.1
    coeff_calorie_6: float = 2.0
    LEN_STEP: float = 1.38

    def __init__(
                 self, 
                 action: int, 
                 duration: float, 
                 weight: float,
                 length_pool: float, 
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool
        
    def get_distance(self) -> float:
        return (self.action * self.count_pool) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.coeff_calorie_5)
                * self.coeff_calorie_6 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    read: Dict[str, type] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type in read:
        return read[workout_type](*data)
    else:
        print(f'{workout_type} что это такое?')


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
