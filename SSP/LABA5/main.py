import random
import json


class Component:
    def __init__(self, name, characteristics):
        self.name = name
        self.characteristics = characteristics

    def __str__(self):
        return f"{self.name}: {', '.join([f'{key}: {value}' for key, value in self.characteristics.items()])}"


class CPU(Component):
    def __init__(self, name, frequency, cores):
        characteristics = {"частота": frequency, "ядра": cores}
        super().__init__(name, characteristics)


class GPU(Component):
    def __init__(self, name, memory, frequency):
        characteristics = {"память": memory, "частота": frequency}
        super().__init__(name, characteristics)


class PSU(Component):
    def __init__(self, name, power, efficiency):
        characteristics = {"мощность": power, "эффективность": efficiency}
        super().__init__(name, characteristics)


class PC:
    def __init__(self, components=None):
        self.components = components if components else []

    def __str__(self):
        pc_info = [str(component) for component in self.components]
        return '\n'.join(pc_info)

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, component):
        if component in self.components:
            self.components.remove(component)
            return True
        else:
            return False

    def total_power(self):
        total_power = sum(int(component.characteristics.get("мощность", 0).split()[0]) for component in self.components if isinstance(component, PSU))
        return f"Общая мощность ПК: {total_power} W"

    def compare(self, other_pc):
        # Implement comparison logic based on desired attributes
        pass


class Inventory:
    def __init__(self):
        self.components = []
        self.pcs = {}

    def add_component(self, component):
        self.components.append(component)

    def add_pc(self, pc):
        self.pcs[len(self.pcs) + 1] = pc

    def remove_item(self, inventory_type):
        if inventory_type == 'компоненты' or inventory_type == '1':
            item_name = input("Введите название компонента для удаления: ")
            self.components = [component for component in self.components if component.name != item_name]
        elif inventory_type == 'пк' or inventory_type == '2':
            pc_index = int(input("Введите индекс пк для удаления: "))
            if pc_index in self.pcs:
                del self.pcs[pc_index]

    def show_inventory(self, choice):
        if choice == 'компоненты' or choice == '1':
            print("Компоненты:")
            for component in self.components:
                print(component)
        elif choice == 'пк' or choice == '2':
            print("ПК:")
            for index, pc in self.pcs.items():
                print(f"Индекс: {index}")
                print(pc)

    def find_pc_with_highest_cpu_frequency(self):
        highest_frequency_pc = None
        highest_frequency = 0
        for pc in self.pcs.values():
            for component in pc.components:
                if isinstance(component, CPU):
                    frequency = float(component.characteristics["частота"].split()[0])
                    if frequency > highest_frequency:
                        highest_frequency = frequency
                        highest_frequency_pc = pc
        return highest_frequency_pc


def create_pc(components):
    cpu_options = [component for component in components if isinstance(component, CPU)]
    gpu_options = [component for component in components if isinstance(component, GPU)]
    psu_options = [component for component in components if isinstance(component, PSU)]

    if cpu_options and gpu_options and psu_options:
        cpu = random.choice(cpu_options)
        gpu = random.choice(gpu_options)
        psu = random.choice(psu_options)
        pc = PC([cpu, gpu, psu])
        components.remove(cpu)
        components.remove(gpu)
        components.remove(psu)
        return pc
    else:
        print("Недостаточно компонентов для сборки ПК.")
        return None


def main():
    inventory = Inventory()

    for _ in range(3):
        inventory.add_component(CPU(f"CPU_{random.randint(1, 100)}", f"{random.uniform(2, 5):.2f} GHz", random.randint(2, 16)))
        inventory.add_component(GPU(f"GPU_{random.randint(1, 100)}", f"{random.randint(4, 12)} GB", f"{random.randint(1000, 2000)} MHz"))
        inventory.add_component(PSU(f"PSU_{random.randint(1, 100)}", f"{random.randint(400, 1000)} W", f"{random.randint(80, 95)}%"))

    while True:
        print("\n1. Показать инвентарь\n2. Создать ПК\n3. Удалить предмет\n4. Найти ПК с самым высокочастотным процессором\n5. Выход")
        choice = input("Что делаем?: ")

        if choice == '1':
            inventory_type = input("Введите тип предмета (компоненты/пк): ")
            inventory.show_inventory(inventory_type)

        elif choice == '2':
            pc = create_pc(inventory.components)
            if pc:
                inventory.add_pc(pc)
                print("ПК создан.")

        elif choice == '3':
            inventory_type = input("Введите тип предмета (компоненты/пк): ")
            inventory.remove_item(inventory_type)

        elif choice == '4':
            pc_with_highest_frequency = inventory.find_pc_with_highest_cpu_frequency()
            if pc_with_highest_frequency:
                print(f"ПК с самым высокочастотным процессором:\n{pc_with_highest_frequency}")
            else:
                print("ПК не найден.")

        elif choice == '5':
            print("Выход...")
            break

        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()
