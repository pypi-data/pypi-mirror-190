# coding: utf-8
import json
import requests

from django import forms
from sentry.plugins.bases import notify

WECHAT_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"

class WechatWebhookOptionsForm(notify.NotificationConfigurationForm):
    key = forms.CharField(
        max_length=255,
        help_text='默认企业微信webHookKey',
        required = True
    )
    prod_key = forms.CharField(
        max_length=255,
        help_text="生产企业微信webHookKey,为空则通过默认Key发送消息"
    )


class MultiWechatWebhookPlugin(notify.NotificationPlugin):
    author = 'badx'
    author_url = 'https://github.com/badx/sentry-multi-webhook'
    version = '0.0.3'
    description = u'Sentry 企业微信 Webhook 插件'
    resource_links = [
        ('Source', 'https://github.com/badx/sentry-multi-webhook'),
        ('Bug Tracker', 'https://github.com/badx/sentry-multi-webhook/issues'),
        ('README', 'https://github.com/badx/sentry-multi-webhook/blob/master/README.md'),
    ]

    slug = 'multi_wechat_webhook'
    title = 'Multi Wechat Webhook'
    conf_key = slug
    conf_title = title
    project_conf_form = WechatWebhookOptionsForm

    def is_configured(self, project, **kwargs):
        return bool(self.get_option('key', project))

    def notify_users(self, group, event, fail_silently=False, **kwargs):
        key = self.get_option('key', group.project)
        prod_key = self.get_option("prod_key", group.project)
        with open("/home/sentry/log/message.log") as f:
            f.write(json.dumps(event))
            f.write("*" * 30)
        url = WECHAT_WEBHOOK_URL.format(key=key)
        if prod_key and event.project.slug.endswith("prod") or \
                (event.environment and event.environment.startswith("prod")):
            url = WECHAT_WEBHOOK_URL.format(key=prod_key)

        title = u"有新的通知来自 {} 项目".format(event.project.slug +
                                        (event.environment if (not event.project.slug.endswith("prod") and
                                                               not event.project.slug.endswith("int")
                                                               and event.environment) else ""))
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": u"#### {title} \n > {message} \n [查看]({url})".format(
                    title=title,
                    message=event.message,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.event_id),
                )
            }
        }
        requests.post(
            url=url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )