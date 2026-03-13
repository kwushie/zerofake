1. Download anaconda/miniconda
2. Create a new python environment with ```conda env create -f env.yaml```
3. Activate the environment with ```conda activate zerofake```

You also need to download the spacy model by:

```
python -m spacy download en_core_web_sm
```

### Reconstruction

You can reconstruct the given image by:

```
python uni-ddim-inversion.py --target image-directory-path --output output-directory-path
```

Then you can compute the similarity between the original images and the reconstructed images by:

```
python sim.py --orginal image-directory-path1 --reconstruct image-directory-path2 
```

A sample dataset is in IMDB-WIKI_small
