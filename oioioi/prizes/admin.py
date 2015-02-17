from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from oioioi.base import admin
from oioioi.base.utils import make_html_link
from oioioi.contests.admin import ContestAdmin
from oioioi.prizes.models import PrizeGiving, Prize, PrizeForUser
from oioioi.prizes.forms import PrizeGivingForm, PrizeInlineFormSet


class PrizeGivingInline(admin.TabularInline):
    model = PrizeGiving
    form = PrizeGivingForm
    extra = 0
    readonly_fields = ('state_with_link',)

    def state_with_link(self, instance):
        if not instance.report:
            return instance.state

        if instance.id is not None:
            href = reverse('oioioi.prizes.views.download_report_view',
                           kwargs={'pg_id': instance.id,
                                   'contest_id': instance.contest.id})
            return make_html_link(href, instance.state)
        return None
    state_with_link.short_description = _("state")

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'key':
            kwargs['choices'] = [(key, value[0]) for key, value in
                    request.contest.controller.get_prizes_distributors()
                    .iteritems()]
        return super(PrizeGivingInline, self).formfield_for_choice_field(
                db_field, request, **kwargs)


class PrizeInline(admin.TabularInline):
    model = Prize
    formset = PrizeInlineFormSet
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'prize_giving':
            kwargs['queryset'] = \
                    PrizeGiving.objects.filter(contest=request.contest)
        return super(PrizeInline, self) \
                .formfield_for_foreignkey(db_field, request, **kwargs)


class PrizesAdminMixin(object):
    def __init__(self, *args, **kwargs):
        super(PrizesAdminMixin, self).__init__(*args, **kwargs)
        self.inlines = self.inlines + [PrizeGivingInline, PrizeInline]

    def save_related(self, request, *args, **kwargs):
        super(PrizesAdminMixin, self).save_related(request, *args, **kwargs)

        if not request.contest:
            return

        pgs_for_scheduling = request.contest.prizegiving_set \
                .select_for_update() \
                .filter(state='NOT_SCHEDULED', date__isnull=False)

        for pg in pgs_for_scheduling:
            pg.schedule()


ContestAdmin.mix_in(PrizesAdminMixin)
admin.site.register(PrizeForUser)