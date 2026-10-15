"""Загрузка блоков маршрута и правил из seed_data."""

from django.db import transaction

from apps.routes.models import ContentBlock, ContentBlockLink, RouteRule
from apps.surveys.models import Question, Scenario


@transaction.atomic
def load_route_content(scenario_slug, blocks, overwrite=False):
    scenario = Scenario.objects.get(slug=scenario_slug)
    stats = {"created": 0, "existing": 0}

    for index, data in enumerate(blocks, start=1):
        fields = {"scenario": scenario, "role": ContentBlock.Role.STEP, "title": data["title"], "body": data["body"]}
        if overwrite:
            block, created = ContentBlock.objects.update_or_create(code=data["code"], defaults=fields)
        else:
            block, created = ContentBlock.objects.get_or_create(code=data["code"], defaults=fields)
        stats["created" if created else "existing"] += 1

        if created or overwrite:
            block.links.all().delete()
            ContentBlockLink.objects.bulk_create([
                ContentBlockLink(block=block, order=i, label=l["label"], kind=l["kind"], target=l["target"])
                for i, l in enumerate(data["links"], start=1)
            ])

        step_question = Question.objects.get(scenario=scenario, code=data["step"])
        rule_fields = {"condition": data["condition"], "position": index * 10, "step_question": step_question}
        rule = RouteRule.objects.filter(scenario=scenario, block=block).first()
        if rule is None:
            RouteRule.objects.create(scenario=scenario, block=block, **rule_fields)
        elif overwrite:
            for name, value in rule_fields.items():
                setattr(rule, name, value)
            rule.save()
    return stats
