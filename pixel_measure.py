# TODO:
# ! Record mouse positions after each click.
# ! Calculate the distance after two clicks.
# ! Determine the ratio between the distances.
# ! Features:
# ? Freeze the screen (like Snipping Tool does)
# ? Add a toggle display for showing the click positions
# ?  (may require freezing the screen as an image)
# ? Allow zoom-in


from pynput.mouse import Listener as m_Listener
# from pynput.keyboard import Listener as kb_Listener
import logging


# Global position list of tuples
pos = []
# Global state for whether the mouse has been clicked once before
clicked = False


def on_click(x, y, button, pressed):
    """ When the mouse is clicked, record the cursor position. """
    global pos, clicked

    if not pressed:
        # Break out if a full click (down and up) does not occur
        return True

    logging.info(f"On-click point: ({x}, {y})")

    pos.append((x, y))

    # Computes the total distance between all points in the list
    if clicked:
        distance = compute_distance(pos)
        print(distance)
        pos = []

    clicked = not clicked


def main():
    # Open up the mouse event listener
    with m_Listener(on_click=on_click) as listener:
        listener.join()


def compute_distance(pos: list) -> float or bool:
    """ Computes the distance between each point in the list sequentially.
        Returns the sum of the points. If the computation was not successful,
        it returns a False value.
    """
    if len(pos) <= 1:
        print("Big mistake buddy. You need TWO or more points selected.")
        return False
    else:
        # Compute distance
        distance = 0
        for ind, point in enumerate(pos):
            if ind + 1 >= len(pos):
                break
            x1, y1 = point
            x2, y2 = pos[ind + 1]
            logging.info(f"Distance points: ({x1}, {y1}), ({x2},{y2})")
            distance += ((y2 - y1)**2 + (x2 - x1)**2)**0.5

        return distance


if __name__ == '__main__':
    main()
