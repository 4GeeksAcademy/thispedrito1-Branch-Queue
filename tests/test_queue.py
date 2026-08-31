import unittest

from triage_queue import EmptyQueueError, InvalidTriageLevelError, Patient, TriageQueue


class TestPatientValidation(unittest.TestCase):
    def test_empty_name_raises(self) -> None:
        with self.assertRaises(ValueError):
            Patient(name="   ", triage_level=1)

    def test_invalid_triage_level_raises(self) -> None:
        with self.assertRaises(InvalidTriageLevelError):
            Patient(name="Ana", triage_level=4)


class TestTriageQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = TriageQueue()

    def test_dequeue_priority_order(self) -> None:
        self.queue.enqueue(Patient(name="Paciente 3", triage_level=3))
        self.queue.enqueue(Patient(name="Paciente 2", triage_level=2))
        self.queue.enqueue(Patient(name="Paciente 1", triage_level=1))

        self.assertEqual(self.queue.dequeue().name, "Paciente 1")
        self.assertEqual(self.queue.dequeue().name, "Paciente 2")
        self.assertEqual(self.queue.dequeue().name, "Paciente 3")

    def test_fifo_within_same_level(self) -> None:
        self.queue.enqueue(Patient(name="Luis", triage_level=2))
        self.queue.enqueue(Patient(name="Maria", triage_level=2))
        self.queue.enqueue(Patient(name="Carlos", triage_level=2))

        self.assertEqual(self.queue.dequeue().name, "Luis")
        self.assertEqual(self.queue.dequeue().name, "Maria")
        self.assertEqual(self.queue.dequeue().name, "Carlos")

    def test_peek_does_not_remove(self) -> None:
        self.queue.enqueue(Patient(name="Elena", triage_level=1))

        first = self.queue.peek()
        self.assertEqual(first.name, "Elena")
        self.assertEqual(len(self.queue), 1)

    def test_list_queue_returns_attention_order(self) -> None:
        self.queue.enqueue(Patient(name="Sergio", triage_level=3))
        self.queue.enqueue(Patient(name="Noa", triage_level=1))
        self.queue.enqueue(Patient(name="Irene", triage_level=2))

        ordered_names = [patient.name for patient in self.queue.list_queue()]
        self.assertEqual(ordered_names, ["Noa", "Irene", "Sergio"])

    def test_stats_counts_by_level(self) -> None:
        self.queue.enqueue(Patient(name="A", triage_level=1))
        self.queue.enqueue(Patient(name="B", triage_level=1))
        self.queue.enqueue(Patient(name="C", triage_level=3))

        self.assertEqual(self.queue.stats(), {1: 2, 2: 0, 3: 1})

    def test_dequeue_empty_queue_raises(self) -> None:
        with self.assertRaises(EmptyQueueError):
            self.queue.dequeue()

    def test_peek_empty_queue_raises(self) -> None:
        with self.assertRaises(EmptyQueueError):
            self.queue.peek()


if __name__ == "__main__":
    unittest.main()
