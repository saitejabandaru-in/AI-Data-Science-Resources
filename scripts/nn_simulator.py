#!/usr/bin/env python3
import time
import math

# Training data for logic gates
GATE_DATA = {
    "AND": [
        ([0, 0], 0),
        ([0, 1], 0),
        ([1, 0], 0),
        ([1, 1], 1)
    ],
    "OR": [
        ([0, 0], 0),
        ([0, 1], 1),
        ([1, 0], 1),
        ([1, 1], 1)
    ]
}

class Perceptron:
    def __init__(self, learning_rate=0.2):
        self.w = [0.1, -0.2]  # Initial weights
        self.b = 0.0          # Initial bias
        self.lr = learning_rate

    def predict(self, x):
        # Activation = weight_1 * x_1 + weight_2 * x_2 + bias
        z = self.w[0] * x[0] + self.w[1] * x[1] + self.b
        # Step function activation
        return 1 if z >= 0 else 0

    def train_step(self, x, target):
        prediction = self.predict(x)
        error = target - prediction
        if error != 0:
            # Update weights: W = W + lr * error * X
            self.w[0] += self.lr * error * x[0]
            self.w[1] += self.lr * error * x[1]
            self.b += self.lr * error
        return abs(error)

def render_decision_boundary(model, grid_size=9):
    """Renders a 2D ASCII grid showing the neuron's classification boundary."""
    grid = []
    # Loop over y-coordinates (top to bottom)
    for y_idx in range(grid_size - 1, -1, -1):
        y = y_idx / (grid_size - 1)
        row_chars = []
        # Loop over x-coordinates (left to right)
        for x_idx in range(grid_size):
            x = x_idx / (grid_size - 1)
            
            # Predict classification at this coordinate point
            pred = model.predict([x, y])
            
            # Mark decision boundary boundary
            if pred == 1:
                row_chars.append("█ ") # Class 1
            else:
                row_chars.append(". ") # Class 0
        grid.append("".join(row_chars))
    return "\n".join(grid)

def main():
    print("="*60)
    print("🧠  AI Lab: Visual Single-Neuron (Perceptron) Simulator  🧠")
    print("="*60)
    print("This simulator visualizes how a single artificial neuron learns")
    print("to partition space in real-time to solve logic gates.\n")

    # Let user select gate
    print("Select a logical function to train the neuron on:")
    print("  [1] AND Gate (Only fires when both inputs are 1)")
    print("  [2] OR Gate (Fires when at least one input is 1)")
    
    choice = input("Select gate (1 or 2, default: 1): ").strip()
    gate_name = "OR" if choice == "2" else "AND"
    data = GATE_DATA[gate_name]

    print(f"\n⚡ Training Perceptron for logical {gate_name} gate...")
    print("Wait 1.5 seconds, training starting soon...")
    time.sleep(1.5)

    model = Perceptron()
    epochs = 12

    for epoch in range(1, epochs + 1):
        total_error = 0
        # Train on all 4 patterns
        for x, target in data:
            error = model.train_step(x, target)
            total_error += error
            
        # Visual animation rendering
        # Clear screen code for terminals
        print("\033[H\033[J", end="")
        print("="*60)
        print(f"Epoch {epoch}/{epochs} | Total Error: {total_error}")
        print(f"Weights: W1 = {model.w[0]:.2f}, W2 = {model.w[1]:.2f} | Bias: b = {model.b:.2f}")
        print("="*60)
        print("ASCII Decision Space View:")
        print("('.' = predicted 0, '█' = predicted 1)\n")
        print(render_decision_boundary(model))
        print("="*60)
        print("Training patterns status:")
        for x, target in data:
            pred = model.predict(x)
            status = "✅" if pred == target else "❌"
            print(f"  Input: {x} -> Target: {target} | Predicted: {pred} {status}")
        print("="*60)
        
        # Slow down for animation effect
        time.sleep(0.35)

    print("\n🎉 Training Complete!")
    if total_error == 0:
        print("The neuron successfully found a linear decision boundary separating the classes!")
    else:
        print("Maximum epochs reached. Adjust learning rate or run again.")
    print("")

if __name__ == "__main__":
    main()
