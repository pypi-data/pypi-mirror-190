import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from syndb_cassandra.utils.misc import get_class_names


class Axon(Model):
    __table_name__ = "axon"

    dataset_id = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    terminal_count = columns.Integer()
    mitochondria_count = columns.Integer()
    total_mitochondria_volume = columns.Float()

    # ==================================================================================================================

    voxel_volume = columns.Float()

    mesh_volume = columns.Float()
    mesh_surface_area = columns.Float()
    mesh_area_volume_ratio = columns.Float()
    mesh_sphericity = columns.Float()

    centroid_z = columns.Float()
    centroid_x = columns.Float()
    centroid_y = columns.Float()

    parent_id = columns.UUID()
    parent_table_name = columns.Ascii()

    cid = columns.UUID(default=uuid.uuid4(), db_field="id")
    neuron_id = columns.UUID()


class PreSynapticTerminal(Model):
    __table_name__ = "pre_synaptic_terminal"

    dataset_id = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    vesicle_count = columns.Integer()
    total_vesicle_volume = columns.Float()

    mitochondria_count = columns.Integer()
    total_mitochondria_volume = columns.Float()

    forms_synapse_with = columns.UUID()

    # ==================================================================================================================

    voxel_volume = columns.Float()

    mesh_volume = columns.Float()
    mesh_surface_area = columns.Float()
    mesh_area_volume_ratio = columns.Float()
    mesh_sphericity = columns.Float()

    centroid_z = columns.Float()
    centroid_x = columns.Float()
    centroid_y = columns.Float()

    parent_id = columns.UUID()
    parent_table_name = columns.Ascii()

    cid = columns.UUID(default=uuid.uuid4(), db_field="id")
    neuron_id = columns.UUID()


class DendriticSpine(Model):
    __table_name__ = "dendritic_spine"

    dataset_id = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    forms_synapse_with = columns.UUID()

    # ==================================================================================================================

    voxel_volume = columns.Float()

    mesh_volume = columns.Float()
    mesh_surface_area = columns.Float()
    mesh_area_volume_ratio = columns.Float()
    mesh_sphericity = columns.Float()

    centroid_z = columns.Float()
    centroid_x = columns.Float()
    centroid_y = columns.Float()

    parent_id = columns.UUID()
    parent_table_name = columns.Ascii()

    cid = columns.UUID(default=uuid.uuid4(), db_field="id")
    neuron_id = columns.UUID()


class Dendrite(Model):
    __table_name__ = "dendrite"

    dataset_id = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    post_synaptic_terminal_count = columns.Integer()
    dendritic_spine_count = columns.Integer()

    # ==================================================================================================================

    voxel_volume = columns.Float()

    mesh_volume = columns.Float()
    mesh_surface_area = columns.Float()
    mesh_area_volume_ratio = columns.Float()
    mesh_sphericity = columns.Float()

    centroid_z = columns.Float()
    centroid_x = columns.Float()
    centroid_y = columns.Float()

    parent_id = columns.UUID()
    parent_table_name = columns.Ascii()

    cid = columns.UUID(default=uuid.uuid4(), db_field="id")
    neuron_id = columns.UUID()


dendrite_axon_models = (
    Axon,
    PreSynapticTerminal,
    DendriticSpine,
    Dendrite,
)
dendrite_axon_model_names = get_class_names(dendrite_axon_models)
