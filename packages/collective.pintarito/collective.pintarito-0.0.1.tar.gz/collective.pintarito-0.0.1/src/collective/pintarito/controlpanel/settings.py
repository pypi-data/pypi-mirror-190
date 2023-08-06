from collective.pintarito import _
from plone.app.registry.browser import controlpanel
from zope import schema
from zope.interface import Interface


class IPintaritoSettings(Interface):
    """Global pintarito settings.

    This describes records stored in the configuration registry and
    obtainable via plone.registry.
    """

    selection = schema.Choice(
        title=_("Selection"),
        description=_("Default selection"),
        vocabulary="collective.pintarito.vocabularies.available_selections",
        default="red",
    )


class PintaritoSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IPintaritoSettings
    schema_prefix = "pintarito.settings"
    label = _("label_pintarito_settings", default="Pintarito settings")
    description = _(
        "description_pintarito_settings",
        default="Below are some options for configuring Pintarito.",
    )


class PintaritoSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PintaritoSettingsEditForm
