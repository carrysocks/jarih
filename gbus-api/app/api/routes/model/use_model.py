# import package
import torch
import torch.nn as nn
import pandas as pd
import os

# LSTM Model architecture
class LSTMModel(nn.Module):
    def __init__(self):
        super(LSTMModel, self).__init__()
        self.window_size = 5
        self.input_size = 6
        self.hidden_size = 64
        self.num_layers = 5
        self.dropout = 0.1
        self.n_steps = 5
        output_size = 1
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # LSTM layers
        self.lstm1 = nn.LSTM(
            input_size, hidden_size, num_layers, batch_first=True, dropout=dropout
        )
        self.lstm2 = nn.LSTM(
            hidden_size, hidden_size, num_layers, batch_first=True, dropout=dropout
        )

        # Fully connected layer
        self.fc = nn.Linear(hidden_size, self.n_steps * output_size)

    def forward(self, x):
        batch_size = x.size(0)

        # Initialize hidden state and cell state for lstm1
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)

        out, (h_n, c_n) = self.lstm1(x, (h0.detach(), c0.detach()))
        out, _ = self.lstm2(out, (h_n, c_n))

        # Pass the output of the LSTM layers through the fully connected layer
        out = self.fc(out[:, -1, :])
        out = out.view(batch_size, n_steps, output_size)

        return out

    def inference(self, input_data, route_id):

        model_path = f"app/api/routes/model/models/{route_id}.pth"
        
        try:
            model.load_state_dict(torch.load(model_path))
        except (FileNotFoundError, RuntimeError) as e:
            raise e 

        # input_data.reverse()
        # print(input_data)

        input_data = (
            torch.tensor(input_data)
            .reshape(1, self.window_size, self.input_size)
            .to(device)
            .float()
        )
        with torch.no_grad():
            output = model(input_data)
        predictions = output.squeeze().tolist()
        predictions = [int(num) for num in predictions]
        return predictions

# Hyper parpameter
window_size = 5
input_size = 6
hidden_size = 64
num_layers = 5
dropout = 0.1
n_steps = 5
output_size = 1

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = LSTMModel().to(device)
# model.load_state_dict(torch.load("app/api/routes/model/219000013_mult_window.pth"))
# model = model.to("cuda")


input_data = [
    [57, 16, 0, 3, 4, 0],
    [59, 16, 1, 3, 4, 0],
    [60, 16, 1, 3, 4, 0],
    [63, 16, 1, 3, 4, 0],
    [63, 16, 1, 3, 4, 0],
]
