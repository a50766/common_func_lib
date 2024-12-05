from django.db import transaction
import requests, xmltodict

class DefineURL:
    
    base_protocol = str('https')
    base_url = None
    base_port = str('443') if 'https' in base_protocol else str('80')
    path = None
    params = {}
    
    def _define_url(self):
        """
        Method define a URL based on self attributes, returning it as string
        """
        url = f'{self.base_protocol}://{self.base_url}:{self.base_port}'
        
        if self.path:
            url += self.path
        
        if self.params:
            op = '?'
            for key, value in self.params.items():
                op += f'{key}={value}&'
            
            url += op[:-1]
        
        return url


class FetchExternalXMLData(DefineURL):
    
    def __init__(self, url):
        self.base_url = url
    
    def _fetch_data(self, path, params):
        """
        Method fetches an endpoint that returns a XML, decode it and parse it into a dictionary
        """
        self.path = path
        self.params = params
        external_api_url = self._define_url()
        #print("URL da API:", external_api_url)
        xml_data = requests.get(external_api_url).content.decode('utf-8')
        return xmltodict.parse(xml_data)


class BasicSerializerOperation:
    
    def __init__(self, logger):
        self.logger = logger
    
    @transaction.atomic
    def create_entity(self, serializer_class, data):
        """
        Method serialize and save (create) a data dictionary
            serializer_class: the serializer class wanted to save the dictionary
            data: mapped dictionary
        """
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return True, instance
        else:
            #self.logger.error(serializer.errors)
            print("Error while creating entity:", serializer.errors)
            return False, None
    
    @transaction.atomic
    def update_entity(self, serializer_class, instance, data, partial=False):
        """
        Method serialize and save (update) a data dictionary
            serializer_class: the serializer class wanted to save the dictionary
            instance: target model instance
            data: mapped dictionary
            partial: True if only some fields will be updated, False if all fields will be updated
        """
        serializer = serializer_class(instance=instance, data=data, partial=partial)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return True, updated_instance
        else:
            #self.logger.error(serializer.errors)
            print("Error while creating entity:", serializer.errors)
            return False, None