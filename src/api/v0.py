import logging
import os

import nltk
import orjson
from fastapi import APIRouter, Response
from fastapi.responses import ORJSONResponse
from starlette.status import HTTP_204_NO_CONTENT
from pydantic import BaseModel

from src.core.find_context import find_context, get_file_paths, read_and_tokenize

logger = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def create_router() -> APIRouter:
    router = APIRouter()

    class ContextRequest(BaseModel):
        word: str
        length: int
        count: int

    @router.post(
        "/context",
        name="Get context",
        response_class=ORJSONResponse,
    )
    async def get_context(request: ContextRequest):
        context = find_context(
            read_and_tokenize(get_file_paths()),
            word=request.word,
            length=request.length,
            count=request.count,
        )

        return ORJSONResponse(content={"context": context})

    @router.options("/context")
    async def get_context_opts():
        return Response(
            status_code=HTTP_204_NO_CONTENT,
            headers={
                "Allow": "OPTIONS, GET, PUT, POST",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET, PUT",
                "Access-Control-Allow-Headers": "X-Custom-Header",
            },
        )

    class WordsRequest(BaseModel):
        text: str

    @router.post(
        "/words",
        name="Get words",
        response_class=ORJSONResponse,
    )
    async def get_words(request: WordsRequest):
        words_with_info = dict()
        corpus_file = os.path.join(CURRENT_DIR, "..", "..", "animals_corpus.json")
        if not os.path.isfile(corpus_file):
            raise Exception("corpus does not exists")

        with open(corpus_file, "r") as file:
            corpus = orjson.loads(file.read())

        for word in nltk.word_tokenize(request.text, language="russian"):
            try:
                if corpus[word]["frequency"] != 0:
                    words_with_info[word] = corpus[word]
            except KeyError:
                continue

        print(words_with_info)

        return ORJSONResponse(content=words_with_info)

    @router.options("/words")
    async def get_words_opts():
        return Response(
            status_code=HTTP_204_NO_CONTENT,
            headers={
                "Allow": "OPTIONS, GET, PUT, POST",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET, PUT",
                "Access-Control-Allow-Headers": "X-Custom-Header",
            },
        )

    return router
