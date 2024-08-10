from rest_framework import serializers

from tasks.models import Paragraph, TokenizedWords
from tasks.helpers import tokenized_words

class ParagraphSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(read_only=True, source='user.email')
    uuid = serializers.CharField(read_only=True)
    paragraphs = serializers.CharField(read_only=True)
    text = serializers.CharField(write_only=True)

    class Meta:
        model = Paragraph
        fields = [
            'user',
            'uuid',
            'paragraphs',
            'text'
        ]

    def create(self, data):
        text = data.pop('text',None)
        user = self.context['request'].user
        if text:
            # Tokenize and split paragraphs
            each_para, indexed_words = tokenized_words(text)

            for para_id, para_text in each_para.items():
                # Save each paragraph to the database
                paragraph = Paragraph.objects.create(
                    user=user,
                    uuid=para_id,
                    paragraphs=para_text
                )

                # Save each tokenized word with its index
                for word_dict in indexed_words[para_id]:
                    for word, idx in word_dict.items():
                        TokenizedWords.objects.create(
                            user = user,
                            uuid=paragraph,
                            words=word,
                            indexes=idx
                        )

            return paragraph
        return None
        

class TokenizedSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')  # Display user's email
    paragraph_uuid = serializers.CharField(source='uuid.uuid')

    class Meta:
        model = TokenizedWords
        fields = [
            'user',
            'paragraph_uuid',
            'indexes',
            'words',
        ]
