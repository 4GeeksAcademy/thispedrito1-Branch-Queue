from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque, Dict, List


class EmptyQueueError(Exception):
    """Raised when trying to read/remove a patient from an empty queue."""


class InvalidTriageLevelError(ValueError):
    """Raised when a triage level is outside the accepted range (1-3)."""


@dataclass(slots=True)
class Patient:
    name: str
    triage_level: int
    arrived_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        cleaned_name = self.name.strip()
        if not cleaned_name:
            raise ValueError("Patient name cannot be empty.")

        if self.triage_level not in (1, 2, 3):
            raise InvalidTriageLevelError(
                "Triage level must be 1 (critical), 2 (urgent), or 3 (standard)."
            )

        self.name = cleaned_name


class TriageQueue:
    def __init__(self) -> None:
        self._queues: Dict[int, Deque[Patient]] = {1: deque(), 2: deque(), 3: deque()}

    def enqueue(self, patient: Patient) -> None:
        self._queues[patient.triage_level].append(patient)

    def dequeue(self) -> Patient:
        for level in (1, 2, 3):
            queue = self._queues[level]
            if queue:
                return queue.popleft()
        raise EmptyQueueError("Cannot dequeue from an empty triage queue.")

    def peek(self) -> Patient:
        for level in (1, 2, 3):
            queue = self._queues[level]
            if queue:
                return queue[0]
        raise EmptyQueueError("Cannot peek into an empty triage queue.")

    def list_queue(self) -> List[Patient]:
        ordered: List[Patient] = []
        for level in (1, 2, 3):
            ordered.extend(self._queues[level])
        return ordered

    def stats(self) -> Dict[int, int]:
        return {level: len(self._queues[level]) for level in (1, 2, 3)}

    def __len__(self) -> int:
        return sum(len(queue) for queue in self._queues.values())


def _format_patient(patient: Patient) -> str:
    timestamp = patient.arrived_at.strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"{patient.name} | triage={patient.triage_level} "
        f"| arrived_at={timestamp}"
    )


def _ask_patient_name() -> str:
    while True:
        name = input("Nombre del paciente: ").strip()
        if name:
            return name
        print("Error: el nombre no puede estar vacio.")


def _ask_triage_level() -> int:
    while True:
        raw = input("Nivel de triaje (1=critico, 2=urgente, 3=estandar): ").strip()
        try:
            level = int(raw)
        except ValueError:
            print("Error: debes introducir un numero entre 1 y 3.")
            continue

        if level in (1, 2, 3):
            return level

        print("Error: nivel invalido. Usa 1, 2 o 3.")


def _print_queue(queue: TriageQueue) -> None:
    patients = queue.list_queue()
    if not patients:
        print("La cola esta vacia.")
        return

    print("\nPacientes en espera (orden de atencion):")
    for index, patient in enumerate(patients, start=1):
        print(f"{index}. {_format_patient(patient)}")


def _print_stats(queue: TriageQueue) -> None:
    counts = queue.stats()
    total = len(queue)
    print("\nEstadisticas:")
    print(f"Nivel 1 (critico): {counts[1]}")
    print(f"Nivel 2 (urgente): {counts[2]}")
    print(f"Nivel 3 (estandar): {counts[3]}")
    print(f"Total en espera: {total}")


def run_cli() -> None:
    queue = TriageQueue()

    menu = (
        "\n--- Gestor de Cola de Triage ---\n"
        "1. Anadir paciente\n"
        "2. Llamar siguiente paciente\n"
        "3. Ver cola actual\n"
        "4. Ver estadisticas\n"
        "5. Ver siguiente (peek)\n"
        "6. Salir\n"
    )

    while True:
        print(menu)
        option = input("Selecciona una opcion (1-6): ").strip()

        if option == "1":
            name = _ask_patient_name()
            level = _ask_triage_level()
            patient = Patient(name=name, triage_level=level)
            queue.enqueue(patient)
            print(f"Paciente agregado: {_format_patient(patient)}")

        elif option == "2":
            try:
                patient = queue.dequeue()
                print(f"Siguiente paciente: {_format_patient(patient)}")
            except EmptyQueueError as exc:
                print(f"Aviso: {exc}")

        elif option == "3":
            _print_queue(queue)

        elif option == "4":
            _print_stats(queue)

        elif option == "5":
            try:
                patient = queue.peek()
                print(f"Proximo paciente: {_format_patient(patient)}")
            except EmptyQueueError as exc:
                print(f"Aviso: {exc}")

        elif option == "6":
            print("Saliendo del gestor. Hasta luego.")
            break

        else:
            print("Error: opcion invalida. Elige un numero del 1 al 6.")


if __name__ == "__main__":
    run_cli()
