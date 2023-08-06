from docstruct import Character, TextBlock


class TextBlockSplitter:
    def __init__(self, text_block: TextBlock, byte_threshold: int, encoding: str):
        self.text_block = text_block
        self.threshold = byte_threshold
        self.encoding = encoding
        self.chunks: list[list[TextBlock]] = []
        self.text_blocks_size: dict[TextBlock:int] = {}
        self.set_text_byte_size(text_block)

        self.current_chunk = []
        self.current_chunk_size = 0
        self.current_chunk_type = None

    def set_text_byte_size(self, text_block: TextBlock):
        byte_size = 0
        if type(text_block) == Character:
            self.text_blocks_size[text_block] = len(
                text_block.get_text().encode(self.encoding)
            )
            return
        if not text_block.children:
            self.text_blocks_size[text_block] = 0
            return
        for child in text_block.children:
            self.set_text_byte_size(child)
            byte_size += self.text_blocks_size[child]
        byte_size += (len(text_block.children) - 1) * len(
            text_block.delimiter.encode(self.encoding)
        )
        self.text_blocks_size[text_block] = byte_size

    def add_current_chunk(self):
        if not self.current_chunk:
            return
        self.chunks.append(self.current_chunk)
        self.current_chunk = []
        self.current_chunk_size = 0
        self.current_chunk_type = None

    def _split_to_chunks(self, text_block: TextBlock):

        type_condition = type(text_block) == self.current_chunk_type
        if self.current_chunk:
            new_size = (
                self.current_chunk_size
                + self.text_blocks_size[text_block]
                + len(text_block.parent.delimiter.encode(self.encoding))
            )
        else:
            new_size = self.text_blocks_size[text_block]

        # add to current chunk case 1
        if type_condition and new_size <= self.threshold:
            self.current_chunk.append(text_block)
            self.current_chunk_size = new_size
            return

        # add to current chunk case 2
        if not self.current_chunk and new_size <= self.threshold:
            self.current_chunk.append(text_block)
            self.current_chunk_size = new_size
            self.current_chunk_type = type(text_block)
            return

        # add the current chunk to the chunks list and clean it
        self.add_current_chunk()

        if self.text_blocks_size[text_block] <= self.threshold:
            self.current_chunk.append(text_block)
            self.current_chunk_size = self.text_blocks_size[text_block]
            self.current_chunk_type = type(text_block)
            return
        else:
            for child in text_block.children:
                self._split_to_chunks(child)

    def get_chunks(self) -> list[list[TextBlock]]:
        self._split_to_chunks(self.text_block)
        self.add_current_chunk()
        return self.chunks
