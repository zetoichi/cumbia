from typing import Type, Sequence, Optional

from django.db import models

class SortableManager(models.Manager):

    def _sort(self, seq: Optional[Sequence[Type[models.Model]]] = None,
            start: int = 0) -> None:
        """
        - Take a sequence of objects and
        - Sort then upwards from start
        """
        if seq is None:
            seq = self
        [obj.assign_idx(start + i) for i, obj in enumerate(seq, 1)]

    def _moving_up(self, new_idx: int, old_idx: int) -> bool:
        """Determine sorting strategy"""
        return new_idx < old_idx

    def initial_sort(self):
        self._sort()

    def insort(self, obj: Type[models.Model], new_idx: int) -> None:
        old_idx = obj.display_idx

        if new_idx != old_idx:
            if self._moving_up(new_idx, old_idx):
                self.insort_right(obj, new_idx)
            else:
                self.insort_left(obj, new_idx)

    def insort_right(self, obj: Type[models.Model], new_idx: int) -> None:
        """
        Move object up, shift rest of sequence right.
        """
        start = new_idx
        self._sort(self.filter(display_idx__gte=new_idx), start)
        obj.assign_idx(new_idx)

    def insort_left(self, obj: Type[models.Model], new_idx: int) -> None:
        """
        Move object down, shift rest of sequence left.
        """
        self._sort(self.filter(display_idx__lte=new_idx)[1:])
        obj.assign_idx(new_idx)

    def sort_incoming(self, seq: Sequence[models.Model]) -> None:
        """
        Assign display order to new pics,
        starting from last element in self.pics
        """
        start = self.count()
        self._sort(seq, start)

    def create(self, *args, **kwargs):
        kwargs['display_idx'] = self.count() + 1
        return super().create(*args, **kwargs)

class PhotographerManager(SortableManager):
    pass

class PicManager(SortableManager):
    pass
