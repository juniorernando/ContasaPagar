# Exemplo de handler para Lambda (API Gateway)
def lambda_handler(event, context):
    # Aqui você faria a validação, instanciaria o serviço e salvaria a conta
    return {
        'statusCode': 200,
        'body': 'Conta criada com sucesso!'
    }
