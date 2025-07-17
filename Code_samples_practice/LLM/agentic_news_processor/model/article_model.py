from typing import Any, Optional
from pydantic import BaseModel

class ArticleModel(BaseModel):
    article_id : Optional [str]
    title : Optional [str]
    description : Optional [str]
    content : Optional [str]
    reworded_title : Optional [str]
    reworded_description : Optional [str]
    reworded_content : Optional [str]
    gpt_category_raw : Optional [str] = None
    recommended_category : Optional [str] = None
    article_image_original : Optional [str]
    processing_status : Optional [str]
    timestamp : Optional [Any]