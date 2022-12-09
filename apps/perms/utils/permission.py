from django.db.models import QuerySet, Model
from collections.abc import Iterable
from assets.models import Node, Asset
from common.utils import get_logger

from perms.models import AssetPermission

logger = get_logger(__file__)

__all__ = ['AssetPermissionUtil']


class AssetPermissionUtil(object):
    """ 资产授权相关的方法工具 """

    def get_permissions_for_user(self, user, with_group=True, flat=False):
        """ 获取用户的授权规则 """
        perm_ids = set()
        # user
        user_perm_ids = AssetPermission.users.through.objects.filter(user_id=user.id) \
            .values_list('assetpermission_id', flat=True).distinct()
        perm_ids.update(user_perm_ids)
        # group
        if with_group:
            groups = user.groups.all()
            group_perm_ids = self.get_permissions_for_user_groups(groups, flat=True)
            perm_ids.update(group_perm_ids)
        if flat:
            return perm_ids
        perms = self.get_permissions(ids=perm_ids)
        return perms

    def get_permissions_for_user_groups(self, user_groups, flat=False):
        """ 获取用户组的授权规则 """
        if isinstance(user_groups, list):
            group_ids = [g.id for g in user_groups]
        else:
            group_ids = user_groups.values_list('id', flat=True).distinct()
        group_perm_ids = AssetPermission.user_groups.through.objects \
            .filter(usergroup_id__in=group_ids) \
            .values_list('assetpermission_id', flat=True).distinct()
        if flat:
            return group_perm_ids
        perms = self.get_permissions(ids=group_perm_ids)
        return perms

    def get_permissions_for_assets(self, assets, with_node=True, flat=False):
        """ 获取资产的授权规则"""
        perm_ids = set()
        assets = self.transform_to_queryset(assets, Asset)
        asset_ids = [str(a.id) for a in assets]
        relations = AssetPermission.assets.through.objects.filter(asset_id__in=asset_ids)
        asset_perm_ids = relations.values_list('assetpermission_id', flat=True).distinct()
        perm_ids.update(asset_perm_ids)
        if with_node:
            nodes = Asset.get_all_nodes_for_assets(assets)
            node_perm_ids = self.get_permissions_for_nodes(nodes, flat=True)
            perm_ids.update(node_perm_ids)
        if flat:
            return perm_ids
        perms = self.get_permissions(ids=perm_ids)
        return perms

    def get_permissions_for_nodes(self, nodes, with_ancestor=False, flat=False):
        """ 获取节点的授权规则 """
        nodes = self.transform_to_queryset(nodes, Node)
        if with_ancestor:
            nodes = Node.get_ancestor_queryset(nodes)
        node_ids = nodes.values_list('id', flat=True).distinct()
        relations = AssetPermission.nodes.through.objects.filter(node_id__in=node_ids)
        perm_ids = relations.values_list('assetpermission_id', flat=True).distinct()
        if flat:
            return perm_ids
        perms = self.get_permissions(ids=perm_ids)
        return perms

    def get_permissions_for_user_asset(self, user, asset):
        """ 获取同时包含用户、资产的授权规则 """
        user_perm_ids = self.get_permissions_for_user(user, flat=True)
        asset_perm_ids = self.get_permissions_for_assets([asset], flat=True)
        perm_ids = set(user_perm_ids) & set(asset_perm_ids)
        perms = self.get_permissions(ids=perm_ids)
        return perms

    def get_permissions_for_user_group_asset(self, user_group, asset):
        user_perm_ids = self.get_permissions_for_user_groups([user_group], flat=True)
        asset_perm_ids = self.get_permissions_for_assets([asset], flat=True)
        perm_ids = set(user_perm_ids) & set(asset_perm_ids)
        perms = self.get_permissions(ids=perm_ids)
        return perms

    @staticmethod
    def get_permissions(ids):
        perms = AssetPermission.objects.filter(id__in=ids).order_by('-date_expired')
        return perms

    @staticmethod
    def transform_to_queryset(objs_or_ids, model):
        if not objs_or_ids:
            return objs_or_ids
        if isinstance(objs_or_ids, QuerySet):
            return objs_or_ids
        ids = [str(o.id) if isinstance(o, model) else o for o in objs_or_ids]
        return model.objects.filter(id__in=ids)


