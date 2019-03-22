import torch
from vlibs import fileio
from vocoder.model import WaveRNN
from vocoder.vocoder_dataset import VocoderDataset
from vocoder import audio
from vocoder.params import *
import numpy as np

run_name = 'mu_law'
model_dir = 'checkpoints'
model_fpath = fileio.join(model_dir, run_name + '.pt')

model = WaveRNN(rnn_dims=512,
              fc_dims=512,
              bits=bits,
              pad=pad,
              upsample_factors=(5, 5, 8),
              feat_dims=80,
              compute_dims=128,
              res_out_dims=128,
              res_blocks=10,
              hop_length=hop_length,
              sample_rate=sample_rate).cuda()

checkpoint = torch.load(model_fpath)
step = checkpoint['step']
model.load_state_dict(checkpoint['model_state'])

data_path = 'E:\\Datasets\\Synthesizer'
gen_path = 'model_outputs'
fileio.ensure_dir(gen_path)

dataset = VocoderDataset(data_path)

# Generate Samples
target = 11000
overlap = 550
k = step // 1000
indices = np.array(range(len(dataset)))
np.random.shuffle(indices)
for i in indices:
    print('Generating...')
    mel, wav_gt = dataset[i]
    
    out_gt_fpath = fileio.join(gen_path, "%s_%dk_steps_%d_gt.wav" % (run_name, k, i))
    out_pred_fpath = fileio.join(gen_path, "%s_%dk_steps_%d_pred.wav" % (run_name, k, i))
    
    wav_gt = audio.restore_signal(wav_gt)
    wav_pred = model.generate(mel, True, target, overlap)
    if use_mu_law:
        import numpy as np
        wav_pred = np.sign(wav_pred) * (1 / (2 ** bits - 1)) * \
              ((1 + (2 ** bits - 1)) ** np.abs(wav_pred) - 1) 

    audio.save_wav(out_pred_fpath, wav_pred)
    audio.save_wav(out_gt_fpath, wav_gt)


