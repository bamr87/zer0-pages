import pytest
from unittest.mock import patch

@pytest.mark.django_db
@patch('ai.services.OpenAIProvider.generate')
def test_ai_generate(mock_generate, api_client, editor_user):
    api_client.force_authenticate(user=editor_user)
    mock_generate.return_value = "Generated content"
    
    data = {'prompt': 'Test prompt'}
    response = api_client.post('/api/ai/generate/', data)
    
    assert response.status_code == 200
    assert response.data['result'] == "Generated content"
    mock_generate.assert_called_once()

