from Snake import Snake
from Structures.ExplorationNode import ExplorationNode
from Structures.UniqueStack import UniqueStack


def _node(x=10, y=10):
    s = Snake()
    s.segments = [(x, y)]
    return ExplorationNode(s)


class TestExplorationNode:
    def test_default_unexplored(self):
        node = _node()
        assert node.is_unexplored()
        assert not node.is_explored()
        assert not node.is_discarded()

    def test_explore(self):
        node = _node()
        node.explore()
        assert node.is_explored()
        assert not node.is_unexplored()
        assert not node.is_discarded()

    def test_discard(self):
        node = _node()
        node.discard()
        assert node.is_discarded()
        assert not node.is_unexplored()
        assert not node.is_explored()

    def test_parent_link(self):
        parent = _node(10, 10)
        child = ExplorationNode(Snake(), parent)
        assert child.parent is parent
        assert parent.parent is None


class TestUniqueStack:
    def test_initial_size(self):
        stack = UniqueStack(_node())
        assert stack.size() == 1
        assert not stack.is_empty()

    def test_push_unique_item(self):
        stack = UniqueStack(_node(5, 5))
        stack.push(_node(6, 5))
        assert stack.size() == 2

    def test_push_duplicate_is_discarded(self):
        stack = UniqueStack(_node(5, 5))
        duplicate = _node(5, 5)
        stack.push(duplicate)
        assert duplicate.is_discarded()
        assert stack.size() == 1

    def test_has_not_discarded_items_true(self):
        stack = UniqueStack(_node())
        assert stack.has_not_discarted_items()

    def test_has_not_discarded_items_false_when_all_discarded(self):
        node = _node()
        stack = UniqueStack(node)
        node.discard()
        assert not stack.has_not_discarted_items()

    def test_get_last_not_discarded(self):
        node = _node()
        stack = UniqueStack(node)
        assert stack.get_last_not_discarded_item() is node

    def test_get_last_not_discarded_skips_discarded(self):
        node1 = _node(5, 5)
        stack = UniqueStack(node1)
        node2 = _node(6, 5)
        stack.push(node2)
        node2.discard()
        assert stack.get_last_not_discarded_item() is node1

    def test_get_last_not_discarded_returns_none_when_empty(self):
        node = _node()
        stack = UniqueStack(node)
        node.discard()
        assert stack.get_last_not_discarded_item() is None

    def test_pop(self):
        node1 = _node(5, 5)
        stack = UniqueStack(node1)
        node2 = _node(6, 5)
        stack.push(node2)
        popped = stack.pop()
        assert popped is node2
        assert stack.size() == 1

    def test_get_last_unexplored_item(self):
        node = _node()
        stack = UniqueStack(node)
        assert stack.get_last_unexplored_item() is node
        node.explore()
        assert stack.get_last_unexplored_item() is None

    def test_get_explored_items(self):
        node = _node()
        stack = UniqueStack(node)
        assert stack.get_explored_items() == []
        node.explore()
        assert stack.get_explored_items() == [node]

    def test_count_unexplored_items(self):
        stack = UniqueStack(_node(5, 5))
        stack.push(_node(6, 5))
        assert stack.count_unexplored_items() == 2

    def test_count_discarded_items(self):
        node = _node()
        stack = UniqueStack(node)
        assert stack.count_discarted_items() == 0
        node.discard()
        assert stack.count_discarted_items() == 1

    def test_count_explored_items(self):
        node = _node()
        stack = UniqueStack(node)
        assert stack.count_explored_items() == 0
        node.explore()
        assert stack.count_explored_items() == 1