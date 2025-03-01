import argparse
import os
os.environ["CUDA_VISIBLE_DEVICES"]="0"
os.environ["FLAGS_use_cuda_managed_memory"]="true"

import paddle
from paddlemix import QWenLMHeadModel

def export(args):
    model = QWenLMHeadModel.from_pretrained(args.model_name_or_path, dtype="float16")
    model.eval()

    # convert to static graph with specific input description
    model = paddle.jit.to_static(
        model.visual,
        input_spec=[
            paddle.static.InputSpec(
                shape=[None, 3, None, None], dtype="float32"),  # images
        ])

    # save to static model
    paddle.jit.save(model, args.save_path)
    print(f"static model has been to {args.save_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        default="qwen-vl/qwen-vl-7b",
        type=str,
        help="The dir name of qwen-vl checkpoint.",
    )
    parser.add_argument(
        "--save_path",
        default="./checkpoints/encode_image/vision",
        type=str,
        help="The saving path of static qwen-vl.",
    )
    args = parser.parse_args()

    export(args)
