from typing import Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = format(duration, '.3f')
        self.distance = format(distance, '.3f')
        self.speed = format(speed, '.3f')
        self.calories = format(calories, '.3f')

    def get_message(self) -> str:
        """Функция для печати сообщения о тренировке."""
        message = (f"Тип тренировки: {self.training_type};"
                   f" Длительность: {self.duration} ч.;"
                   f" Дистанция: {self.distance} км;"
                   f" Ср. скорость: {self.speed} км/ч;"
                   f" Потрачено ккал: {self.calories}.")
        return message


class Training:
    """Базовый класс тренировки."""
    # расстояние, которое спортсмен преодолевает за один шаг.
    LEN_STEP: float = 0.65
    # константа для перевода значений из метров в километры.
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = float(duration)
        self.weight = float(weight)
        self.duration_min = duration * 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        # Формула расчета action * LEN_STEP / M_IN_KM
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # Формула расчета средней скрорости движения
        # преодоленная_дистанция_за_тренировку / время_тренировки
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Установим заглушку так как для каждого вида спорта
        # подсчет колорий свой.
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message_class = InfoMessage(training_type=type(self).__name__,
                                    duration=self.duration,
                                    distance=self.get_distance(),
                                    speed=self.get_mean_speed(),
                                    calories=self.get_spent_calories())
        return message_class


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # вынесем коэффициенты в отдельные переменные
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        # Формула рассчета каллорий
        # (coeff_calorie_1 * средняя_скорость - coeff_calorie_2)
        # * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах
        spent_calories: float = ((coeff_calorie_1 * self.get_mean_speed()
                                 - coeff_calorie_2)
                                 * self.weight / self.M_IN_KM
                                 * self.duration_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # переопределим название тренировки

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # вынесем коэффициенты в отдельные переменные
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        # Формула рассчета каллорий
        # (coeff_calorie_1 * средняя_скорость -
        # coeff_calorie_2) * вес_спортсмена / M_IN_KM *
        # время_тренировки_в_минутах
        spent_calories: float = ((coeff_calorie_1 * self.weight
                                 + (self.get_mean_speed() ** 2
                                  // self.height) * coeff_calorie_2
                                 * self.weight) * self.duration_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    # переопределим расстояние, которое спортсмен преодолевает за один гребок.
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # Формула расчета средней скорости плавания
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        mean_speed: float = ((self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration))
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # вынесем коэффициенты в отдельные переменные
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: float = 2.0
        # Формула рассчета каллорий
        # (средняя_скорость + 1.1) * 2 * вес
        spent_calories: float = ((self.get_mean_speed() + coeff_calorie_1)
                                 * coeff_calorie_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    # Создадим словарь в формате ключ тренировки: класс вида тренировки
    dict_trening: Dict[str, Training] = {'SWM': Swimming,
                                         'RUN': Running,
                                         'WLK': SportsWalking}
    # в переменную get_traning запишем экземпляр класса Training
    # честно говоря мне код который написан ниже и вся эта
    #  конструкция не очень нравится,
    #  как правильно и лучше оформить?
    get_traning: Training = dict_trening[workout_type]
    if workout_type == 'SWM':
        swm_trening: Training = get_traning(action=data[0],
                                            duration=data[1],
                                            weight=data[2],
                                            length_pool=data[3],
                                            count_pool=data[4])
        return swm_trening
    elif workout_type == 'RUN':
        run_trening: Training = get_traning(action=data[0],
                                            duration=data[1],
                                            weight=data[2])
        return run_trening
    elif workout_type == 'WLK':
        wlk_trening: Training = get_traning(action=data[0],
                                            duration=data[1],
                                            weight=data[2],
                                            height=data[3])
        return wlk_trening


def main(training: Training) -> None:
    """Главная функция."""
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
