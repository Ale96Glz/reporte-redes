def calculate_rtt(input_file, output_file, alpha=0.125, beta=0.25, k=4):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write("SampleRTT\tEstimatedRTT\tDevRTT\tTimeoutInterval\n")

        estimated_rtt = None
        dev_rtt = None
        sample_rtts = []
        estimated_rtts = []

        for i, line in enumerate(infile):
            sample_rtt = float(line.strip())
            sample_rtts.append(sample_rtt)

            if i == 0:
                estimated_rtt = sample_rtt
                dev_rtt = sample_rtt / 2
            else:
                estimated_rtt = (1 - alpha) * estimated_rtt + alpha * sample_rtt
                dev_rtt = (1 - beta) * dev_rtt + beta * abs(sample_rtt - estimated_rtt)

            timeout_interval = estimated_rtt + k * dev_rtt

            sample_rtt = round(sample_rtt, 4)
            estimated_rtt = round(estimated_rtt, 4)
            dev_rtt = round(dev_rtt, 4)
            timeout_interval = round(timeout_interval, 4)

            estimated_rtts.append(estimated_rtt)
            outfile.write(f"{sample_rtt}\t{estimated_rtt}\t{dev_rtt}\t{timeout_interval}\n")

    mse = sum((s - e) ** 2 for s, e in zip(sample_rtts, estimated_rtts)) / len(sample_rtts)
    print(f"MSE para alpha={alpha}: {mse}")


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    alpha = float(sys.argv[3]) if len(sys.argv) > 3 else 0.125
    beta = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25
    k = float(sys.argv[5]) if len(sys.argv) > 5 else 4

    calculate_rtt(input_file, output_file, alpha, beta, k)
