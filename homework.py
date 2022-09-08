from dataclasses import dataclass
from typing import Dict, List, Type, Union, ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.
    Args:
        training_type (str): имя класса тренировки.
        duration Union[int, float]: длительность тренировки в часах.
        distance Union[int, float]: дистанция в километрах, которую преодолел
            пользователь за время тренировки.
        speed Union[int, float]: средняя скорость, с которой двигался пользователь.
        calories Union[int, float] количество килокалорий, которое израсходовал
            пользователь за время тренировки.
    """
    training_type: str
    duration: Union[int, float]
    distance: Union[int, float]
    speed: Union[int, float]
    calories: Union[int, float]

    def get_message(self) -> str:
        """Функция для печати сообщения о тренировке.
        Returns:
            str: сообщние для вывода
        """
        return (f"Тип тренировки: {self.training_type};"
                f" Длительность: {self.duration:0.3f} ч.;"
                f" Дистанция: {self.distance:0.3f} км;"
                f" Ср. скорость: {self.speed:0.3f} км/ч;"
                f" Потрачено ккал: {self.calories:0.3f}.")


class Training:
    """Базовый класс тренировки, инициализируется следующими данными.
    Args:
        LEN_STEP (float): расстояние, которое
            спортсмен преодолевает за один шаг.
        M_IN_KM (int): константа для перевода значений из метров в километры.
        MINUTES_IN_HOUR (int): константа в которую
            записываю сколько в минут в часе
    """
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MINUTES_IN_HOUR: ClassVar[int] = 60

    def __init__(self,
                 action: int,
                 duration: Union[int, float],
                 weight: Union[int, float],
                 ) -> None:
        """На вход базовый класс принимает
        Args:
            action (int): количество совершенных действий шагов/гребков
            duration Union[int, float]: длительность тренировки  в минутах
            weight Union[int, float]: вес спортсмена
        Returns: 
            None
        """
        self.action = action
        self.duration = float(duration)
        self.weight = float(weight)

    def get_distance(self) -> float:
        """Получить дистанцию в км.
        Returns:
            float: дистанцию в км       
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.
        Returns:
               float: средняя скорость.        
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Raises:
            NotImplementedError: если метод не переопредел, после вызова кидаем исключение
        """
        # Установим заглушку так как для каждого вида спорта
        # подсчет колорий свой.
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке.
        Return:
            InfoMessage: экземпляр класса сообщений
        """
        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег.
        Args:
            COEFF_CALORIE_1 Union[int,float]: коэффициент для расчета калорий.
            COEFF_CALORIE_2 Union[int,float]: коэффициент для расчета калорий.
    """
    COEFF_CALORIE_1: ClassVar[Union[int, float]] = 18
    COEFF_CALORIE_2: ClassVar[Union[int, float]] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
            Returns:
                float: количпство затраченных калорий
        """
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MINUTES_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
        Args:
            COEFF_CALORIE_1 Union[int,float]: коэффициент для расчета калорий.
            COEFF_CALORIE_2 Union[int,float]: коэффициент для расчета калорий.
    """
    COEFF_CALORIE_1: ClassVar[Union[int, float]] = 0.035
    COEFF_CALORIE_2: ClassVar[Union[int, float]] = 0.029

    def __init__(self,
                 action: int,
                 duration: Union[int, float],
                 weight: Union[int, float],
                 height: Union[int, float]) -> None:
        """Класс спортивной ходьбы инициализируется
        Args:
            action (int): количество совершенных действий шагов/гребков
            duration Union[int, float]: длительность тренировки  в минутах
            weight Union[int, float]: вес спортсмена
            height Union[int, float]: рост спортсмена
        Returns: 
            None
        """
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
            Returns:
                float: количество затраченных калорий
        """
        return ((self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** 2
                // self.height) * self.COEFF_CALORIE_2
                * self.weight) * (self.duration
                * self.MINUTES_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание.
        Args:
        LEN_STEP (float): расстояние, которое
            спортсмен преодолевает за один гребок.
            COEFF_CALORIE_1 Union[int,float]: коэффициент для расчета калорий.
            COEFF_CALORIE_2 Union[int,float]: коэффициент для расчета калорий.
    """
    COEFF_CALORIE_1: ClassVar[Union[int, float]] = 1.1
    COEFF_CALORIE_2: ClassVar[Union[int, float]] = 2.0
    LEN_STEP: ClassVar[float] = 1.38

    def __init__(self,
                 action: int,
                 duration: Union[int, float],
                 weight: Union[int, float],
                 length_pool: Union[int, float],
                 count_pool: Union[int, float]) -> None:
        """Класс плавания инициализируется следующими данными
        Args:
            action (int): количество совершенных действий шагов/гребков
            duration Union[int, float]: длительность тренировки  в минутах
            weight Union[int, float]: вес спортсмена
            length_pool Union[int, float]: длина бассейна в метрах
            count_pool (Union[int, float]: сколько раз пользователь переплыл бассейн
        Returns: 
            None
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.
            Returns:
                float: средняя скорость движения
        """
        return ((self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration))

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
            Returns:
                float: количество затраченных калорий
        """
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков.
        Args:
            workout_type str: название тронировки
            data: List[int]: данные тренировки и спортсмена
        Returns:
            Training: класс вида тренировки
    """
    # Создадим словарь в формате ключ, тренировка: класс вида тренировки
    trening_matching: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking}
    return trening_matching[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция для вывода сообзщения о тренировки.
        Args:
            training Training: класс типа тренировки
        Returns:
            None
    """
    info: InfoMessage = training.show_training_info()
    print(info.get_message())
    return None


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
