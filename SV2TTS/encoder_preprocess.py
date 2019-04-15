from encoder.preprocess import preprocess_librispeech, preprocess_voxceleb1, preprocess_voxceleb2
from pathlib import Path
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocesses audio files from datasets, encodes them as mel spectrograms and "
                    "writes them to the disk.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("datasets_root", type=str, help=\
        "Path to the directory containing your LibriSpeech/TTS and VoxCeleb datasets.")
    parser.add_argument("-o", "--out_dir", type=str, default=argparse.SUPPRESS, help=\
        "Path to the output directory that will contain the mel spectrograms. If left out, "
        "defaults to <datasets_root>/SV2TTS/encoder/")
    parser.add_argument("-d", "--datasets", type=str, 
                        default="librispeech_other,voxceleb1,voxceleb2", help=\
        "Comma-separated list of datasets you want to preprocess. Only the train set of these "
        "datasets will be used.")
    parser.add_argument("-s", "--skip_existing", action="store_true", help=\
        "Whether to overwrite existing files with the same name. Useful if the preprocessing was "
        "interrupted.")

    # Reformat the arguments
    args = parser.parse_args()
    args.datasets_root = Path(args.datasets_root)
    args.datasets = args.datasets.split(",")
    if not hasattr(args, "out_dir"):
        args.out_dir = Path(args.datasets_root, "SV2TTS", "encoder")
    args.out_dir = Path(args.out_dir)
    args.out_dir.mkdir(exist_ok=True)
    
    # Preprocess the datasets
    preprocess_func = {
        "librispeech_other": preprocess_librispeech,
        "voxceleb1": preprocess_voxceleb1,
        "voxceleb2": preprocess_voxceleb2,
    }
    args = vars(args)
    for dataset in args.pop("datasets"):
        print("Preprocessing %s" % dataset)
        preprocess_func[dataset](**args)
