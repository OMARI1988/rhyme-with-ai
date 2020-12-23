![](screenshot.gif)

## Local development

Create a [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) virtual environment and activate it:

```bash
conda env create --file environment.yml
conda activate rhyme-with-ai
```

Install the `rhyme_with_ai` package and all its dependencies:

```bash
pip install --editable .
```

Download the weights of the models (if you get any errors, make sure these align with those specified in `app/app.py`)):

```bash
make download-data
```

Run the app:

```bash
python app/app.py
```

And you're done!


## Todo

* Integrate TokenWeighter in the RhymeGenerator.
* Don't block on model loading or rhyme mutations (use API?).
