import copy
from mc_block import McBlock
from mc_class import McClass
from tsml_error import TSMLerror


def post_process(parsed_model):
    model_classes = parsed_model.classes
    for block in parsed_model.blocks:
        replace_identifiers_by_objects(block, block.blocks + model_classes)


def replace_identifiers_by_objects(block, classes):
    for inner_block in block.blocks:
        if isinstance(inner_block, McBlock):
            replace_identifiers_by_objects(inner_block, block.blocks)

    objects = {}
    for class_name in block.class_instances:
        mc_class = get_object_by_name(class_name, classes)

        for identifier in block.class_instances[class_name]:
            class_with_identifier = copy.copy(mc_class)
            class_with_identifier.identifier = identifier
            objects[identifier] = class_with_identifier

    block.class_instances = list(objects.values())

    for synchronization in block.synchronizations:
        if synchronization.name is None:
            identifier = synchronization.event_path.parent
            if identifier not in objects:
                raise TSMLerror('ClassIdentifier ' + identifier + ' not found')
            synchronization.event_path.parent = objects[identifier]
        else:
            for event_path in synchronization.event_paths:
                identifier = event_path.parent
                if identifier not in objects:
                    raise TSMLerror('ClassIdentifier ' + identifier + ' not found')
                event_path.parent = objects[identifier]


def get_object_by_name(name, objects):
    for mc_object in objects:
        if mc_object.name == name:
            return mc_object

    raise TSMLerror('Class or Block with name ' + name + ' not found')