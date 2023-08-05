from django import template
from django.apps import apps
from django.conf import settings
from django.db.models import Prefetch
from django.urls import reverse
from obapi.models import ContentItem

from obpages.models import UserSequence
from obpages.templatetags.constants import OBPAGES_COMPONENTS_PATH

OBPAGES_SECTIONS_PATH = f"{OBPAGES_COMPONENTS_PATH}/sections"
RESULTS_PER_SECTION = getattr(settings, "OBPAGES_RESULTS_PER_SECTION", 5)

register = template.Library()


@register.inclusion_tag(f"{OBPAGES_SECTIONS_PATH}/query_results.html")
def query_results(
    query_results,
    title=None,
    detailed=False,
    row=False,
    max_results=None,
    is_staff=False,
):
    if max_results is not None:
        query_results = query_results[0:max_results]

    return {
        "query_results": query_results,
        "title": title,
        "row": row,
        "detailed": detailed,
        "is_staff": is_staff,
    }


@register.inclusion_tag(f"{OBPAGES_SECTIONS_PATH}/explore_section.html")
def explore_section(model_name, max_results=None):
    model_class = apps.get_model("obapi", model_name)
    item_count = model_class.objects.count()

    if max_results is not None:
        items = list(model_class.objects.all()[0:max_results])
    else:
        items = list(model_class.objects.all())

    more_count = item_count - len(items)

    return {
        "verbose_name": model_class._meta.verbose_name,
        "url": reverse("explore_list", kwargs={"model_name": model_name}),
        "items": items,
        "item_count": item_count,
        "more_count": more_count,
    }


@register.inclusion_tag(f"{OBPAGES_SECTIONS_PATH}/sequence_section.html")
def sequence_section(section, max_results=None):
    all_sequences = UserSequence.objects.all()
    if section == "curated":
        title = "Recent Curated Sequences"
        queryset = all_sequences.filter(curated=True)
        more_url = reverse("sequence_curated_list")
    elif section == "user":
        title = "Recent User-Created Sequences"
        queryset = all_sequences.filter(public=True)
        more_url = reverse("sequence_public_list")

    sequence_count = queryset.count()

    if max_results is not None:
        items = list(queryset[0:max_results])
    else:
        items = list(queryset)

    more_count = sequence_count - len(items)

    return {
        "title": title,
        "verbose_name": "Sequence",
        "url": more_url,
        "items": items,
        "item_count": sequence_count,
        "more_count": more_count,
    }


@register.inclusion_tag(f"{OBPAGES_SECTIONS_PATH}/sequence_results.html")
def sequence_results(sequences, user, title=None, max_results=None):
    if max_results is not None:
        sequences = sequences[0:max_results]

    return {"sequences": sequences, "user": user, "title": title}


@register.inclusion_tag(f"{OBPAGES_SECTIONS_PATH}/sequencemember_results.html")
def sequencemember_results(sequence, user, editable=False):
    members = sequence.members.prefetch_related(
        Prefetch("content_item", ContentItem.objects.select_subclasses())
    )

    items = [member.content_item for member in members]

    return {
        "sequence": sequence,
        "items": items,
        "user": user,
        "editable": editable,
    }
