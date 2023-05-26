import os
import yaml


class RatingAdapter:
    with open(os.path.join('config', 'utils', 'rating_adapter.yml')) as file:
        config_dict = yaml.load(file, Loader=yaml.FullLoader)

    @classmethod
    def loading_value(cls):
        """Show this value while request is being processed"""
        return []

    @classmethod
    def default_value(cls, error_message=""):
        """Show value in case of communication/other error"""
        return [{'name': error_message or "Error loading content",
                 'value': 0}]

    @classmethod
    def prepare_rating_output(cls, output_list, region):
        """ Posprocess rating for frontend according to region """
        # pick mapping according to region
        if region.lower() in cls.config_dict['rating_mapping']:
            priority_rating = cls.config_dict['rating_mapping'][region.lower()]
        else:
            priority_rating = cls.config_dict['rating_mapping']['default']

        output_list = cls.process_priority_rating(
            priority_list=cls.config_dict[priority_rating].get('processed_ratings', {}),
            output_list=output_list,
            keep_other=cls.config_dict[priority_rating].get('include_not_processed', False))

        return output_list

    @classmethod
    def process_priority_rating(cls, priority_list, output_list, keep_other=False):
        """ Extract & rename values in priority list in desired order"""
        updated_output_list = []

        # pick rating in a desired order in priority rating list
        for priority_rating in priority_list:
            record_dict_num = 0
            while record_dict_num < len(output_list):
                if output_list[record_dict_num]['name'] == priority_rating['input']:
                    output_list[record_dict_num]['name'] = priority_rating['output']
                    updated_output_list.append(output_list[record_dict_num])

                    output_list = output_list[:record_dict_num] + output_list[record_dict_num + 1:]
                else:
                    record_dict_num += 1

        if keep_other:
            # add other values to the end of the list
            updated_output_list = updated_output_list + output_list
        else:
            # group other values to "Other" category
            other_value = 100 - sum(map(lambda x: x['value'], updated_output_list))
            # constant is used to avoid python float representation inconsistencies
            if other_value > 0.01:
                updated_output_list.append({'name': 'Other', 'value': other_value})

        return updated_output_list
