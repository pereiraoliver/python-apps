from pathlib import Path

import pandas as pd
from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent
pdf = FPDF(orientation="P", unit="mm", format="A4")
df = pd.read_csv(BASE_DIR / "articles.csv", dtype={"id": str})


class Arcticle:
    def __init__(self, article_id):
        self.article_id = article_id

    def exists(self):
        return (df["id"] == self.article_id).any()

    def choose(self):
        df.loc[df["id"] == self.article_id, "in_stock"] -= 1
        df.to_csv(BASE_DIR / "articles.csv", index=False)

    def is_available(self):
        stock = df.loc[df["id"] == self.article_id, "in_stock"].iloc[0]
        return stock > 0

    def print_receipt(self):
        receipt = f"""
Receipt nr.{self.article_id}
Artcle: {df.loc[df["id"] == self.article_id, "name"].iloc[0]}
Price: {df.loc[df["id"] == self.article_id, "price"].iloc[0]}
"""
        print(receipt)
        pdf.add_page()
        pdf.set_font(family="Times", size=16)
        pdf.multi_cell(w=0, h=8, txt=receipt)
        pdf.output(BASE_DIR / "output.pdf")


print(df)
article_id = input("Choose an article to by: ")
article = Arcticle(article_id)
if not article.exists():
    print("Article does not exist")
elif article.is_available():
    article.choose()
    article.print_receipt()
else:
    print("Article not available")
