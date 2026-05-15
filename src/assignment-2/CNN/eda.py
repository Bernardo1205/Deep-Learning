from __future__ import annotations

import os
import sys
import cv2
import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

from pathlib import Path
from PIL import Image
import seaborn as sns

# For t-SNE and UMAP visualizations (heavy)
import torch
import torchvision.models as models
import torchvision.transforms as T
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import umap

from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings("ignore")

# Shared visual theme
SPACE_DARK = "#0d0d1a"
SPACE_BLUE = "#1a1a3e"
ACCENT = "#7b68ee"
ACCENT2 = "#00d4ff"
TEXT_COLOR = "#e8e8f0"
GRID_COLOR = "#2a2a4a"

# One colour per class — order matches sorted(classes)
PALETTE = [
    "#7b68ee",  # asteroid — purple
    "#c0c0c0",  # black_hole — silver
    "#4facfe",  # earth — blue
    "#a8e063",  # galaxy — lime
    "#ff8c42",  # jupiter — orange
    "#ff6b6b",  # mars — red
    "#d4a853",  # mercury — gold-brown
    "#00d4ff",  # neptune — cyan
    "#b0a8d4",  # pluto — lavender
    "#f0c040",  # saturn — yellow
    "#4ecdc4",  # uranus — teal
    "#ff6b9d",  # venus — pink
]

SPACE_CMAP = LinearSegmentedColormap.from_list(
    "space", [SPACE_DARK, ACCENT, ACCENT2], N=256
)

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

plt.rcParams.update({
    "figure.facecolor": "white",  # Set figure background to white
    "axes.facecolor": "white",  # Set axes background to white
    "axes.edgecolor": "black",  # Set axes edge color to black
    "axes.labelcolor": "black",  # Set axes label color to black
    "axes.titlecolor": "black",  # Set axes title color to black
    "xtick.color": "black",  # Set x-tick color to black
    "ytick.color": "black",  # Set y-tick color to black
    "grid.color": "gray",   # Set grid color to gray
    "text.color": "black",  # Set text color to black
    "legend.facecolor": "white",  # Set legend background to white
    "legend.edgecolor": "black",  # Set legend edge color to black
})

IMG_EXTS = {".jpg", ".jpeg", ".png"}

# General Configuration
DATASET_PATH = Path("./dataset")
SPLITS = ["training", "validation", "test"]

# Metadata recopilation
def load_dataset_metadata(dataset_path=DATASET_PATH):
    """
    Walk through the dataset directory structure and collect metadata for each image, including:
        - File path
        - Split (training/validation/test)
        - Class label
        - Image dimensions (width, height)
        - Aspect ratio
        - Number of channels
        - Brightness (mean pixel value)
        - Contrast (standard deviation of pixel values)
        - Sharpness (Laplacian variance)
        - File size (KB)
    Returns a DataFrame with one row per image and the above metadata as columns.
    """
    data = []

    for split in SPLITS:
        split_path = dataset_path / split

        if not split_path.exists():
            continue

        for class_folder in split_path.iterdir():
            if class_folder.is_dir():
                class_name = class_folder.name

                image_paths = []
                extensions = ['*.jpg', '*.jpeg', '*.png']

                for ext in extensions:
                    image_paths.extend(list(class_folder.glob(ext)))

                for img_path in image_paths:
                    try:
                        with Image.open(img_path) as img:
                            width, height = img.size
                            mode = img.mode

                        img_cv = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)

                        if img_cv is not None:
                            brightness = np.mean(img_cv)
                            contrast = np.std(img_cv)
                            sharpness = cv2.Laplacian(img_cv, cv2.CV_64F).var()
                        else:
                            brightness = np.nan
                            contrast = np.nan
                            sharpness = np.nan

                        file_size = os.path.getsize(img_path) / 1024

                        data.append({
                            "path": str(img_path),
                            "split": split,
                            "label": class_name,
                            "width": width,
                            "height": height,
                            "aspect_ratio": width / height,
                            "channels": len(mode) if mode in ['RGB', 'RGBA'] else 1,
                            "brightness": brightness,
                            "contrast": contrast,
                            "sharpness": sharpness,
                            "file_size_kb": file_size,
                            "mode": mode
                        })

                    except Exception as e:
                        print(f"Error reading {img_path}: {e}")

    return pd.DataFrame(data)


# Class Distribution
def plot_class_distribution(df):
    plt.figure(figsize=(14, 7))

    sns.countplot(
        data=df,
        y="label",
        hue="split",
        order=df['label'].value_counts().index,
        palette="viridis"
    )

    plt.title("Class Distribution by Split", fontsize=16, fontweight='bold')
    plt.xlabel("Images Count")
    plt.ylabel("Class")
    plt.tight_layout()
    plt.show()


# Proportion Training | Validation | Test
def plot_split_distribution(df):
    split_counts = df['split'].value_counts()

    plt.figure(figsize=(8, 8))

    plt.pie(
        split_counts,
        labels=split_counts.index,
        autopct='%1.1f%%',
        startangle=140
    )

    plt.title("Splits Distribution")
    plt.tight_layout()
    plt.show()


# Grid of Images
def plot_image_grid(df, samples_per_class=4):
    labels = sorted(df['label'].unique())

    fig, axes = plt.subplots(
        len(labels),
        samples_per_class,
        figsize=(samples_per_class * 3, len(labels) * 3)
    )

    for i, label in enumerate(labels):
        subset = df[df['label'] == label]

        sample_rows = subset.sample(
            min(samples_per_class, len(subset))
        )

        for j in range(samples_per_class):
            ax = axes[i, j]

            if j < len(sample_rows):
                row = sample_rows.iloc[j]
                img = Image.open(row['path'])

                ax.imshow(img)

                if j == 0:
                    ax.set_ylabel(label, fontsize=12, fontweight='bold')

            ax.set_xticks([])
            ax.set_yticks([])

    plt.suptitle("Random Samples per Class", fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.show()


# Image Resolution
def plot_image_resolution(df):
    plt.figure(figsize=(10, 8))

    sns.scatterplot(
        data=df,
        x="width",
        y="height",
        hue="split",
        alpha=0.6,
        palette="Set2"
    )

    max_dim = max(df['width'].max(), df['height'].max())

    plt.plot(
        [0, max_dim],
        [0, max_dim],
        linestyle='--'
    )

    plt.title("Image Resolution (Width vs Height)")
    plt.xlabel("Width")
    plt.ylabel("Height")
    plt.tight_layout()
    plt.show()


# Aspect Ratio Distribution
def plot_aspect_ratio_distribution(df):
    plt.figure(figsize=(12, 6))

    sns.histplot(
        df['aspect_ratio'],
        bins=30,
        kde=True
    )

    plt.title("Aspect Ratio Distribution")
    plt.xlabel("Aspect Ratio")
    plt.ylabel("Frecuency")
    plt.tight_layout()
    plt.show()

# Brightness vs Contrast
def plot_brightness_vs_contrast(df):
    plt.figure(figsize=(12, 8))

    sns.scatterplot(
        data=df,
        x="brightness",
        y="contrast",
        hue="label",
        alpha=0.6,
        palette="turbo"
    )

    plt.title("Brightness vs Contrast")
    plt.xlabel("Brightness")
    plt.ylabel("Contrast")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


# Sharpness Boxplot
def plot_sharpness_boxplot(df):
    plt.figure(figsize=(14, 6))

    sns.boxplot(
        data=df,
        x="label",
        y="sharpness",
        palette="magma"
    )

    plt.yscale('log')

    plt.title("Sharpness (Laplacian Variance) by Class")
    plt.xlabel("Class")
    plt.ylabel("Laplacian Variance (log scale)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Black/Empty Image Analysis
def plot_dark_image_analysis(df):
    dark_images = (df['brightness'] < 20).sum()
    normal_images = (df['brightness'] >= 20).sum()

    categories = ['Black/Empty', 'Normal']
    values = [dark_images, normal_images]

    plt.figure(figsize=(8, 6))

    plt.bar(categories, values)

    plt.title("Black Images Analysis")
    plt.ylabel("Cantity")
    plt.tight_layout()
    plt.show()


def _color_for(cls: str, classes: list[str]) -> str:
    idx = classes.index(cls) if cls in classes else 0
    return PALETTE[idx % len(PALETTE)]


# t-SNE + UMAP of ResNet-18 embeddings
def plot_embedding_projection(
    df,
    split: str = "training",
    n_sample: int = 300,
    input_size: int = 224,
    batch_size: int = 32,
    tsne_perplexity: float = 40.0,
    umap_n_neighbors: int = 20,
    random_state: int = 42,
) -> None:
    """
    Extract ResNet-18 features (ImageNet pretrained, no fine-tuning) and
    project them into 2D with both t-SNE and UMAP.

    Why this matters:
      • If classes form tight, well-separated clusters → the raw visual
        features are already discriminative — the CNN has an easy job.
      • If two classes overlap (e.g. Neptune & Uranus) → expect confusion in
        those classes in the final model. You can verify this against the
        confusion matrix later in the presentation.
      • Outlier points far from their class cluster are likely mislabelled
        or corrupted images.

    The function produces a 1×2 figure: t-SNE (left) | UMAP (right).
    Class centroids are annotated directly on the plot.

    Parameters
    ----------
    df              : DataFrame with columns ["path", "class", "split"]
    split           : which split to sample from
    n_sample        : total images to embed (keep ≤500 for speed)
    input_size      : resize to this square before ResNet (224 or 299)
    batch_size      : GPU/CPU batch size for feature extraction
    tsne_perplexity : t-SNE perplexity (5–50; larger = more global structure)
    umap_n_neighbors: UMAP neighbourhood size (10–50)
    random_state    : reproducibility seed
    """
    print("  Extracting ResNet-18 embeddings and projecting …")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"     Device: {device}")

    # Sample equally from each class
    sub = df[df["split"] == split] if split in df["split"].values else df
    classes = sorted(sub["class"].unique())
    n_cls   = len(classes)
    per_cls = max(1, n_sample // n_cls)

    rng    = np.random.default_rng(random_state)
    paths, labels = [], []
    for cls in classes:
        cls_paths = sub[sub["class"] == cls]["path"].tolist()
        chosen    = rng.choice(cls_paths, size=min(per_cls, len(cls_paths)),
                               replace=False)
        paths.extend(chosen.tolist())
        labels.extend([cls] * len(chosen))

    print(f"     Embedding {len(paths)} images ({per_cls} per class) …")

    # Build feature extractor (ResNet-18, avgpool output = 512-D)
    # Try ImageNet pretrained weights first; fall back to random init if the
    # model hub is unreachable (air-gapped environments, firewalls, etc.).
    try:
        resnet = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        print("     Loaded pretrained ImageNet weights.")
    except Exception:
        resnet = models.resnet18(weights=None)
        print("     ⚠  Could not download pretrained weights — using random "
              "init.\n"
              "        Cluster separability will be lower, but the plot still\n"
              "        shows relative proximity between classes.")
    resnet.fc = torch.nn.Identity()   # remove classifier head → 512 features
    resnet.eval().to(device)

    transform = T.Compose([
        T.Resize((input_size, input_size)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]),
    ])

    # Extract features in batches
    features: list[np.ndarray] = []
    valid_labels: list[str]    = []
    valid_paths:  list[str]    = []

    with torch.no_grad():
        for batch_start in range(0, len(paths), batch_size):
            batch_paths  = paths[batch_start: batch_start + batch_size]
            batch_labels = labels[batch_start: batch_start + batch_size]
            tensors = []
            kept_labels: list[str] = []
            kept_paths:  list[str] = []

            for p, lbl in zip(batch_paths, batch_labels):
                try:
                    img = Image.open(p).convert("RGB")
                    tensors.append(transform(img))
                    kept_labels.append(lbl)
                    kept_paths.append(p)
                except Exception:
                    pass

            if not tensors:
                continue

            batch_tensor = torch.stack(tensors).to(device)
            out = resnet(batch_tensor).cpu().numpy() # (B, 512)
            features.append(out)
            valid_labels.extend(kept_labels)
            valid_paths.extend(kept_paths)

            done = min(batch_start + batch_size, len(paths))
            print(f"     {done}/{len(paths)} images embedded", end="\r")

    print()
    feat_matrix = np.vstack(features)    # (N, 512)
    feat_scaled = StandardScaler().fit_transform(feat_matrix)

    # t-SNE
    print("     Running t-SNE …")
    tsne_2d = TSNE(
        n_components=2,
        perplexity=min(tsne_perplexity, len(feat_scaled) // 4),
        max_iter=1000,
        random_state=random_state,
        init="pca",
        learning_rate="auto",
    ).fit_transform(feat_scaled)

    # UMAP
    print("     Running UMAP …")
    umap_2d = umap.UMAP(
        n_components=2,
        n_neighbors=umap_n_neighbors,
        min_dist=0.1,
        random_state=random_state,
        metric="euclidean",
    ).fit_transform(feat_scaled)

    # Plot
    fig, axes = plt.subplots(
        1, 2,
        figsize=(20, 9),
        gridspec_kw={"wspace": 0.08},
    )
    fig.suptitle(
        "ResNet-18 Embedding Projections  ·  overlapping clusters = similar appearance = expected model confusion",
        fontsize=14, fontweight="bold", color=TEXT_COLOR, y=1.01,
    )

    proj_cfg = [
        (axes[0], tsne_2d, f"t-SNE  (perplexity={tsne_perplexity:.0f})"),
        (axes[1], umap_2d, f"UMAP  (n_neighbors={umap_n_neighbors})"),
    ]

    label_arr = np.array(valid_labels)

    for ax, coords, title in proj_cfg:
        for j, cls in enumerate(classes):
            mask = label_arr == cls
            col  = _color_for(cls, classes)
            ax.scatter(
                coords[mask, 0], coords[mask, 1],
                color=col, alpha=0.55, s=18,
                edgecolors="none", label=cls,
            )

        # Annotate class centroids
        for j, cls in enumerate(classes):
            mask = label_arr == cls
            if mask.sum() == 0:
                continue
            cx, cy = coords[mask, 0].mean(), coords[mask, 1].mean()
            col = _color_for(cls, classes)
            ax.annotate(
                cls.replace("_", " "),
                xy=(cx, cy),
                fontsize=8.5,
                fontweight="bold",
                color=col,
                ha="center",
                va="center",
                bbox=dict(
                    facecolor=SPACE_DARK + "cc",
                    edgecolor=col,
                    boxstyle="round,pad=0.25",
                    linewidth=0.8,
                ),
            )

        ax.set_title(title, color=TEXT_COLOR, fontsize=12, pad=8)
        ax.set_xlabel("Dim 1", fontsize=9)
        ax.set_ylabel("Dim 2", fontsize=9)
        ax.grid(alpha=0.15)
        ax.tick_params(labelsize=7)

    # Shared legend (right margin)
    handles = [
        plt.Line2D([0], [0], marker="o", color="none",
                   markerfacecolor=_color_for(cls, classes),
                   markersize=8, label=cls.replace("_", " ").title())
        for cls in classes
    ]
    fig.legend(
        handles=handles,
        loc="center right",
        bbox_to_anchor=(1.12, 0.5),
        fontsize=9,
        framealpha=0.4,
        title="Class",
        title_fontsize=9,
    )

    # Overlap analysis: find most confused pairs
    # Use t-SNE coords; compute centroid distance for every class pair
    from itertools import combinations

    centroids = {
        cls: tsne_2d[label_arr == cls].mean(axis=0)
        for cls in classes if (label_arr == cls).sum() > 0
    }
    pair_dists = []
    for a, b in combinations(classes, 2):
        if a in centroids and b in centroids:
            d = np.linalg.norm(centroids[a] - centroids[b])
            pair_dists.append((d, a, b))

    pair_dists.sort()
    n_closest = min(5, len(pair_dists))
    closest   = pair_dists[:n_closest]

    # Annotate overlap panel (bottom of t-SNE axis)
    overlap_text = "Closest pairs (potential confusion):\n" + "\n".join(
        f"  {a} ↔ {b}  (d={d:.1f})" for d, a, b in closest
    )
    axes[0].text(
        0.01, 0.01, overlap_text,
        transform=axes[0].transAxes,
        fontsize=7.5, color=TEXT_COLOR, va="bottom", ha="left",
        bbox=dict(facecolor=SPACE_DARK + "dd", edgecolor=GRID_COLOR,
                  boxstyle="round,pad=0.4"),
    )

    print("\n     Closest class pairs in embedding space (potential confusion):")
    for d, a, b in closest:
        print(f"       {a:12s} ↔ {b:12s}   centroid distance = {d:.2f}")

    # _save(fig, output_dir, "EDA_A3_embedding_projection.png")
    plt.show()

# Standalone entry point
def _collect_paths(dataset_path: Path):
    """Minimal path collector (no metadata) for standalone use."""
    records = []
    for split in ["training", "validation", "test"]:
        split_dir = dataset_path / split
        if not split_dir.exists():
            continue
        for class_dir in sorted(split_dir.iterdir()):
            if not class_dir.is_dir():
                continue
            for p in class_dir.iterdir():
                if p.suffix.lower() in IMG_EXTS:
                    records.append({
                        "path":  str(p),
                        "split": split,
                        "class": class_dir.name,
                    })
    return pd.DataFrame(records)


if __name__ == "__main__":

    print("Loading dataset...")

    df = load_dataset_metadata()

    print(f"Total images found: {len(df)}")

    # Visualizations
    plot_class_distribution(df)
    plot_split_distribution(df)
    plot_image_grid(df)
    plot_image_resolution(df)
    plot_aspect_ratio_distribution(df)
    plot_brightness_vs_contrast(df)
    plot_sharpness_boxplot(df)
    plot_dark_image_analysis(df)

    sns.set_theme(style="darkgrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams.update({
        "figure.facecolor": SPACE_DARK,
        "axes.facecolor": SPACE_BLUE,
        "axes.edgecolor": GRID_COLOR,
        "axes.labelcolor": TEXT_COLOR,
        "axes.titlecolor": TEXT_COLOR,
        "xtick.color": TEXT_COLOR,
        "ytick.color": TEXT_COLOR,
        "grid.color": GRID_COLOR,
        "text.color": TEXT_COLOR,
        "legend.facecolor": SPACE_BLUE,
        "legend.edgecolor": GRID_COLOR,
        "font.family": "DejaVu Sans",
        "font.size": 10,
    })

    df = _collect_paths(DATASET_PATH)
    if df.empty:
        print("ERROR: no images found.")
        sys.exit(1)
    print(f"   Images   : {len(df):,} across "
          f"{df['class'].nunique()} classes\n")

    plot_embedding_projection(
        df,
        split="training",
        n_sample=300,
        input_size=224,
        batch_size=32,
        tsne_perplexity=40.0,
        umap_n_neighbors=20,
        random_state=42,
    )