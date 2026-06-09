#!/usr/bin/env python3
import sys
import math
import time
import argparse

def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))

def sigmoid_derivative(a):
    # Derivative of sigmoid in terms of its activation output
    return a * (1.0 - a)

def draw_node(x, w, b, z, a, target, loss, dw=None, db=None):
    # Prints a beautiful ASCII node layout showing inputs and parameters
    print("      Computational Node Diagram")
    print("      ──────────────────────────")
    print(f"      [Input: x={x:.3f}] ──────┐")
    print(f"                               ├───> [Linear: z = w*x + b] ───> [Sigmoid Activation: a] ───> [Loss]")
    print(f"      [Weight: w={w:.4f}] ─────┤            (z={z:.4f})              (a={a:.4f})              (Loss={loss:.4f})")
    print(f"      [Bias: b={b:.4f}] ───────┘")
    print(f"      [Target: y_target={target:.3f}]")
    if dw is not None and db is not None:
        print("\n      --- Backpropagation Flow (Gradients) ---")
        print(f"      dLoss/da = a - y_target = {a - target:+.4f}")
        print(f"      da/dz    = a * (1 - a)   = {sigmoid_derivative(a):.4f}")
        print(f"      dLoss/dw = dLoss/da * da/dz * x = {dw:+.4f}")
        print(f"      dLoss/db = dLoss/da * da/dz * 1 = {db:+.4f}")

def run_visualizer():
    print("="*60)
    print("🎓  Step-by-Step Neural Backpropagation Simulator  🎓")
    print("="*60)
    print("Welcome! Neural networks learn by propagating gradients backward through layers\n"
          "using the calculus chain rule. Let's watch a single neuron train step-by-step.\n")
          
    # Initial Parameters
    x = 1.5
    w = 0.8
    b = -0.5
    target = 0.2
    lr = 0.5
    
    epoch = 0
    
    while True:
        # 1. Forward Pass
        z = w * x + b
        a = sigmoid(z)
        loss = 0.5 * (a - target) ** 2
        
        print(f"\n--- Epoch {epoch} ---")
        draw_node(x, w, b, z, a, target, loss)
        
        print("\nWhat would you like to do?")
        print("  [S] Run Single Backpropagation Step (Explain Calculus)")
        print("  [T] Train Auto (Run 10 Epochs)")
        print("  [R] Reset Parameters")
        print("  [Q] Quit Simulator\n")
        
        choice = input("Enter choice: ").strip().upper()
        if choice == 'Q':
            print("Exiting Backpropagation Simulator. Goodbye!")
            break
            
        elif choice == 'R':
            w = 0.8
            b = -0.5
            epoch = 0
            print("\nParameters reset to initial states.")
            continue
            
        elif choice == 'S':
            # Calculate gradients
            dloss_da = a - target
            da_dz = sigmoid_derivative(a)
            dloss_dz = dloss_da * da_dz
            
            dloss_dw = dloss_dz * x
            dloss_db = dloss_dz * 1.0
            
            # Show node with backprop details
            print("\n" + "="*50)
            print("🔄 BACKPROPAGATION CALCULATION DETAILS:")
            print("="*50)
            draw_node(x, w, b, z, a, target, loss, dloss_dw, dloss_db)
            print("-" * 50)
            print("Mathematical Steps:")
            print(f"  1. How much does Loss change with Activation?")
            print(f"     dLoss/da = (a - y_target) = {a:.3f} - {target:.3f} = {dloss_da:+.4f}")
            print(f"  2. How much does Activation change with Linear Input?")
            print(f"     da/dz = a * (1 - a) = {a:.3f} * (1 - {a:.3f}) = {da_dz:.4f}")
            print(f"  3. How much does Loss change with Weight? (Chain Rule)")
            print(f"     dLoss/dw = dLoss/da * da/dz * dz/dw = {dloss_da:.4f} * {da_dz:.4f} * {x:.3f} = {dloss_dw:+.4f}")
            print(f"  4. Update Weight:")
            print(f"     w = w - (lr * dLoss/dw) = {w:.4f} - ({lr} * {dloss_dw:+.4f}) = {w - lr * dloss_dw:.4f}")
            
            # Perform updates
            w -= lr * dloss_dw
            b -= lr * dloss_db
            epoch += 1
            
            input("\nPress Enter to apply updates and continue...")
            
        elif choice == 'T':
            print("\nRunning 10 epochs of gradient descent...")
            print("| Epoch | Weight (w) | Bias (b) | Activation (a) | Loss (MSE) |")
            print("|-------|------------|----------|----------------|------------|")
            for _ in range(10):
                z = w * x + b
                a = sigmoid(z)
                loss = 0.5 * (a - target) ** 2
                
                print(f"| {epoch:5d} | {w:10.4f} | {b:8.4f} | {a:14.4f} | {loss:10.6f} |")
                
                # Backprop
                dloss_da = a - target
                da_dz = sigmoid_derivative(a)
                dloss_dw = dloss_da * da_dz * x
                dloss_db = dloss_da * da_dz * 1.0
                
                w -= lr * dloss_dw
                b -= lr * dloss_db
                epoch += 1
                time.sleep(0.15)
            print("\n10 Epochs completed successfully!")
            input("Press Enter to continue...")
            
        else:
            print("\n⚠️ Invalid choice. Try again.")

def main():
    parser = argparse.ArgumentParser(description="Run the interactive step-by-step neural backpropagation simulator.")
    args = parser.parse_args()
    run_visualizer()

if __name__ == "__main__":
    main()
