# Sorting Algorithm Visualization

A Python application that provides interactive visualization of various sorting algorithms using Pygame. This project
demonstrates good software engineering practices with clean code architecture, proper separation of concerns, and
comprehensive documentation.

## Features

- **Interactive Visualization**: Watch sorting algorithms work step-by-step
- **Multiple Algorithms**:
    - Bubble Sort
    - Merge Sort
    - Quick Sort
    - Bucket Sort
- **Real-time Animation**: See comparisons and swaps as they happen
- **User Controls**: Start different algorithms and reset the visualization
- **Clean UI**: Intuitive interface with clearly labeled buttons

## Architecture

The application follows object-oriented design principles with clear separation of concerns:

### Core Components

- **`constants.py`**: Centralized configuration and constants
- **`button.py`**: Reusable button component with hover effects
- **`bar_chart.py`**: Visual representation of data as bars
- **`sorting_algorithms.py`**: Algorithm implementations using generators
- **`visualization_app.py`**: Main application coordinator
- **`main.py`**: Application entry point

### Design Principles Applied

1. **Single Responsibility Principle**: Each class has one clear purpose
2. **Open/Closed Principle**: Easy to add new sorting algorithms
3. **Dependency Injection**: Components receive dependencies rather than creating them
4. **Configuration Management**: All constants centralized
5. **Generator Pattern**: Algorithms yield control for smooth animation
6. **Observer Pattern**: Active indices callback for visualization updates

## Installation

### Prerequisites

- Python 3.7 or higher
- Pygame library

### Setup

1. Install Pygame:

```bash
pip install pygame
```

2. Run the application:

```bash
python main.py
```

## Usage

1. **Start Sorting**: Click any algorithm button to begin visualization
2. **Watch Animation**: Observe highlighted bars showing current comparisons
3. **Reset**: Click "Reset" button to return to original state
4. **Try Different Algorithms**: Compare how different algorithms work

### Controls

- **Bubble Sort**: Simple comparison-based algorithm
- **Merge Sort**: Divide-and-conquer recursive algorithm
- **Quick Sort**: Partition-based recursive algorithm
- **Bucket Sort**: Distribution-based sorting algorithm
- **Reset**: Restore original data and stop current animation

## Code Quality Features

### Good Programming Practices Demonstrated

1. **Clear Documentation**: Comprehensive docstrings and comments
2. **Type Hints**: Function parameters and return types documented
3. **Error Handling**: Graceful handling of edge cases
4. **Consistent Naming**: Clear, descriptive variable and function names
5. **Modular Design**: Loosely coupled, highly cohesive components
6. **Configuration Management**: Centralized constants and settings
7. **Performance Optimization**: Double buffering for smooth rendering

### File Structure

```
sorting_visualization/
├── constants.py          # Application constants
├── button.py            # Button UI component
├── bar_chart.py         # Bar chart visualization
├── sorting_algorithms.py # Algorithm implementations
├── visualization_app.py  # Main application class
├── main.py              # Entry point
└── README.md            # Project documentation
```

## Algorithm Details

### Bubble Sort

- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Visualization**: Shows adjacent element comparisons and swaps

### Merge Sort

- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Visualization**: Demonstrates divide-and-conquer approach with recursive merging

### Quick Sort

- **Time Complexity**: O(n log n) average, O(n²) worst case
- **Space Complexity**: O(log n)
- **Visualization**: Shows partitioning around pivot elements

### Bucket Sort

- **Time Complexity**: O(n + k) where k is number of buckets
- **Space Complexity**: O(n + k)
- **Visualization**: Demonstrates distribution into buckets and reconstruction

## Customization

### Adding New Algorithms

1. Add algorithm implementation to `sorting_algorithms.py`:

```python
@staticmethod
def new_algorithm_generator(values, active_indices_callback):
    # Implementation here
    yield
```

2. Add button configuration in `visualization_app.py`:

```python
button_configs = [
    # ... existing algorithms
    ("New Algorithm", COLOR)
]
```

3. Update algorithm mapping:

```python
algorithm_map = {
    # ... existing mappings
    "New Algorithm": SortingAlgorithms.new_algorithm_generator
}
```

### Modifying Appearance

Edit `constants.py` to change:

- Colors
- Window dimensions
- Animation speed
- Font sizes

### Performance Tuning

Adjust these constants in `constants.py`:

- `ANIMATION_DELAY`: Speed of visualization
- `FPS`: Frame rate
- `BUTTON_*`: Button dimensions and spacing

## Technical Implementation

### Generator Pattern for Algorithms

Each sorting algorithm is implemented as a Python generator that yields control back to the main application loop. This
allows for:

- Smooth step-by-step visualization
- Pausable/resumable execution
- Memory-efficient implementation
- Clean separation between algorithm logic and visualization

### Double Buffering

The application uses double buffering to prevent screen flickering:

1. Render all components to an off-screen buffer
2. Transfer complete buffer to screen in one operation
3. Display the final result

### Event-Driven Architecture

The application follows an event-driven pattern:

- User interactions trigger events
- Events are processed in the main loop
- State changes update the visualization
- Rendering occurs after all updates

## Learning Objectives

This project demonstrates:

1. **Software Architecture**: How to structure a medium-sized application
2. **Design Patterns**: Observer, Generator, and Strategy patterns
3. **Object-Oriented Programming**: Encapsulation, inheritance, and polymorphism
4. **Algorithm Visualization**: Making abstract concepts tangible
5. **User Interface Design**: Creating intuitive, responsive interfaces
6. **Code Documentation**: Writing maintainable, well-documented code
7. **Performance Optimization**: Efficient rendering and animation techniques

## Future Enhancements

Potential improvements:

- Sound effects for comparisons and swaps
- Speed control slider
- Step-by-step mode with manual control
- Algorithm performance statistics
- Save/load different datasets
- Export animation as video
- Additional sorting algorithms (Heap Sort, Radix Sort, etc.)
- Comparison mode showing multiple algorithms simultaneously

## Contributing

When adding features or fixes:

1. Follow the existing code style and architecture
2. Add comprehensive documentation
3. Include error handling
4. Test with various input sizes
5. Update this README if needed

## License

This project is provided as an educational example demonstrating good programming practices in Python with Pygame.