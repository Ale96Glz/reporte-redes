import sys
import numpy as np
import matplotlib.pyplot as plt

def calculate_and_plot_rtt(input_file, alpha_values, beta=0.25, k=4):
    with open(input_file, 'r') as file:
        raw_data = file.readlines()
    
    raw_values = []
    for line in raw_data:
        try:
            value = float(line.strip())
            if value > 0:
                raw_values.append(value)
        except ValueError:
            continue

    if len(raw_values) < 130:
        print("Error: Datos insuficientes para el analisis")
        return

    sample_rtt = np.array(raw_values[100:130])

    estimated_rtt = {alpha: [sample_rtt[0]] for alpha in alpha_values}
    dev_rtt = {alpha: [0] for alpha in alpha_values}
    timeout_interval = {alpha: [] for alpha in alpha_values}
    mse = {}

    for alpha in alpha_values:
        for i in range(1, len(sample_rtt)):
            new_est_rtt = (1 - alpha) * estimated_rtt[alpha][-1] + alpha * sample_rtt[i]
            estimated_rtt[alpha].append(new_est_rtt)
            
            new_dev_rtt = (1 - beta) * dev_rtt[alpha][-1] + beta * abs(sample_rtt[i] - new_est_rtt)
            dev_rtt[alpha].append(new_dev_rtt)
            
            timeout_interval[alpha].append(new_est_rtt + k * new_dev_rtt)

        mse[alpha] = np.mean((sample_rtt - np.array(estimated_rtt[alpha]))**2)

    plt.figure(figsize=(15, 10))
    for alpha in alpha_values:
        plt.plot(sample_rtt, label="SampleRTT", marker='o', linestyle='dotted')
        plt.plot(estimated_rtt[alpha], label=f"EstimatedRTT (α={alpha})", linestyle='--')
        plt.plot(timeout_interval[alpha], label=f"TimeoutInterval (α={alpha})", linestyle='-.')
    
    plt.title(f"Analisis del RTT con distintos valores de alpha: Primera Traza")
    plt.xlabel("Número de muestra")
    plt.ylabel("RTT (ms)")
    plt.legend()
    plt.grid()
    plt.show()

    for alpha, error in mse.items():
        print(f"MSE for α={alpha}: {error}")

if __name__ == "__main__":
    input_file = sys.argv[1]
    alpha_values = list(map(float, sys.argv[2:])) if len(sys.argv) > 2 else [0.125, 0.25, 0.0625]
    calculate_and_plot_rtt(input_file, alpha_values)