# Copyright (C) 2008-2011 Dejan Muhamedagic <dmuhamedagic@suse.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from .ordereddict import odict


cib_cli_map = {
    "node": "node",
    "primitive": "primitive",
    "group": "group",
    "clone": "clone",
    "master": "ms",
    "rsc_location": "location",
    "rsc_colocation": "colocation",
    "rsc_order": "order",
    "rsc_ticket": "rsc_ticket",
    "template": "rsc_template",
    "cluster_property_set": "property",
    "rsc_defaults": "rsc_defaults",
    "op_defaults": "op_defaults",
    "acl_target": "acl_target",
    "acl_group": "acl_group",
    "acl_user": "user",
    "acl_role": "role",
    "fencing-topology": "fencing_topology",
    "tag": "tag"
}
container_tags = ("group", "clone", "ms", "master")
clonems_tags = ("clone", "ms", "master")
resource_tags = ("primitive", "group", "clone", "ms", "master", "template")
constraint_tags = ("rsc_location", "rsc_colocation", "rsc_order", "rsc_ticket")
constraint_rsc_refs = ("rsc", "with-rsc", "first", "then")
children_tags = ("group", "primitive")
nvpairs_tags = ("meta_attributes", "instance_attributes", "utilization")
defaults_tags = ("rsc_defaults", "op_defaults")
resource_cli_names = ("primitive", "group", "clone", "ms", "master", "rsc_template")
constraint_cli_names = ("location", "colocation", "collocation", "order", "rsc_ticket")
nvset_cli_names = ("property", "rsc_defaults", "op_defaults")
op_cli_names = ("monitor",
                "start",
                "stop",
                "migrate_to",
                "migrate_from",
                "promote",
                "demote",
                "notify")
ra_operations = ("probe", "monitor", "start", "stop",
                 "promote", "demote", "notify", "migrate_to", "migrate_from")
subpfx_list = {
    "instance_attributes": "instance_attributes",
    "meta_attributes": "meta_attributes",
    "utilization": "utilization",
    "operations": "ops",
    "rule": "rule",
    "expression": "expression",
    "date_expression": "expression",
    "duration": "duration",
    "date_spec": "date_spec",
    "read": "read",
    "write": "write",
    "deny": "deny",
}
acl_rule_names = ("read", "write", "deny")
acl_spec_map = odict({
    "xpath": "xpath",
    "ref": "ref",
    "tag": "tag",
    "attribute": "attribute",
})
# ACLs were rewritten in pacemaker 1.1.12
# this is the new acl syntax
acl_spec_map_2 = odict({
    "xpath": "xpath",
    "ref": "reference",
    "reference": "reference",
    "tag": "object-type",
    "type": "object-type",
    "attr": "attribute",
    "attribute": "attribute"
})

acl_spec_map_2_rev = (('xpath', 'xpath'),
                      ('reference', 'ref'),
                      ('attribute', 'attr'),
                      ('object-type', 'type'))

acl_shortcuts = {
    "meta":
    (r"//primitive\[@id='@@'\]/meta_attributes", r"/nvpair\[@name='@@'\]"),
    "params":
    (r"//primitive\[@id='@@'\]/instance_attributes", r"/nvpair\[@name='@@'\]"),
    "utilization":
    (r"//primitive\[@id='@@'\]/utilization",),
    "location":
    (r"//rsc_location\[@id='cli-prefer-@@' and @rsc='@@'\]",),
    "property":
    (r"//crm_config/cluster_property_set", r"/nvpair\[@name='@@'\]"),
    "nodeattr":
    (r"//nodes/node/instance_attributes", r"/nvpair\[@name='@@'\]"),
    "nodeutil":
    (r"//nodes/node/utilization", r"\[@uname='@@'\]"),
    "node":
    (r"//nodes/node", r"\[@uname='@@'\]"),
    "status":
    (r"/cib/status",),
    "cib":
    (r"/cib",),
}
lrm_exit_codes = {
    "success": "0",
    "unknown": "1",
    "args": "2",
    "unimplemented": "3",
    "perm": "4",
    "installed": "5",
    "configured": "6",
    "not_running": "7",
    "master": "8",
    "failed_master": "9",
}
lrm_status_codes = {
    "pending": "-1",
    "done": "0",
    "cancelled": "1",
    "timeout": "2",
    "notsupported": "3",
    "error": "4",
}
cib_user_attrs = ("validate-with",)
node_states = ("online", "offline", "unclean")
precious_attrs = ("id-ref",)
op_extra_attrs = ("interval",)
rsc_meta_attributes = (
    "allow-migrate", "is-managed", "interval-origin",
    "migration-threshold", "priority", "multiple-active",
    "failure-timeout", "resource-stickiness", "target-role",
    "restart-type", "description", "remote-node", "requires",
)
group_meta_attributes = ("container", )
clone_meta_attributes = (
    "ordered", "notify", "interleave", "globally-unique",
    "clone-max", "clone-node-max", "clone-state", "description",
)
ms_meta_attributes = (
    "master-max", "master-node-max", "description",
)
trace_ra_attr = "trace_ra"
score_types = {'advisory': '0', 'mandatory': 'INFINITY'}
boolean_ops = ('or', 'and')
binary_ops = ('lt', 'gt', 'lte', 'gte', 'eq', 'ne')
binary_types = ('string', 'version', 'number')
unary_ops = ('defined', 'not_defined')
simple_date_ops = ('lt', 'gt')
date_ops = ('lt', 'gt', 'in_range', 'date_spec')
date_spec_names = '''hours monthdays weekdays yearsdays months \
weeks years weekyears moon'''.split()
in_range_attrs = ('start', 'end')
roles_names = ('Stopped', 'Started', 'Master', 'Slave')
actions_names = ('start', 'promote', 'demote', 'stop')
node_default_type = "normal"
node_attributes_keyw = ("attributes", "utilization")
shadow_envvar = "CIB_shadow"
attr_defaults = {
    "node": {"type": "normal"},
    "resource_set": {"sequential": "true", "require-all": "true"},
    "rule": {"boolean-op": "and"},
}
cib_no_section_rc = 6
# Graphviz attributes for various CIB elements.
# Shared for edge and node and graph attributes.
# Keys are graphviz attributes, values are dicts where keys
# are CIB element names and values graphviz values.
# - element "." refers to the whole graph
# - element "class:<ra_class>" refers to primitives of a
#   specific RA class
# - optional_set is a resource_set with require-all set to
#   false
# - group and optional_set are subgraphs (boxes)
graph = {
    ".": {
        "compound": "true",
    },
    "*": {
        "fontname": "Helvetica",
        "fontsize": "11",
    },
    "node": {
        "style": "bold",
        "shape": "box",
        "color": "blue",
    },
    "primitive": {
        "fillcolor": "lightgrey",
        "style": "filled",
    },
    "rsc_template": {
        "fillcolor": "lightgrey",
        "color": "mediumpurple",
        "style": "filled",
    },
    "class:stonith": {
        "shape": "box",
        "style": "dashed",
    },
    "location": {
        "style": "dashed",
        "dir": "none",
    },
    "clone": {
        "color": "red",
    },
    "ms": {
        "color": "maroon",
    },
    "group": {
        "color": "blue",
        "group": "blue",
        "labelloc": "b",
        "labeljust": "r",
        "labelfontsize": "12",
    },
    "optional_set": {
        "style": "dotted",
    },
    "template:edge": {
        "color": "grey64",
        "style": "dotted",
        "arrowtail": "open",
        "dir": "back",
    },
}

prompt = ''
tmp_cib = False
tmp_cib_prompt = "@tmp@"
live_cib_prompt = "live"

simulate_programs = {
    "ptest": "ptest",
    "simulate": "crm_simulate",
}

meta_progs = ("crmd", "pengine", "stonithd", "cib")
# elide these properties from tab completion
crmd_metadata_do_not_complete = ("dc-version",
                                 "cluster-infrastructure",
                                 "crmd-integration-timeout",
                                 "crmd-finalization-timeout",
                                 "expected-quorum-votes")
extra_cluster_properties = ("dc-version",
                            "cluster-infrastructure",
                            "last-lrm-refresh",
                            "cluster-name")
pcmk_version = ""  # set later

# r.group(1) transition number (a different thing from file number)
# r.group(2) contains full path
# r.group(3) file number
transition_patt = [
    # transition start
    "pengine.* process_pe_message: .*Transition ([0-9]+): .*([^ ]*/pe-[^-]+-(%%)[.]bz2)",
    # r.group(1) transition number (a different thing from file number)
    # r.group(2) contains full path
    # r.group(3) transition status
    # transition stop
    "crmd.* run_graph: .*Transition ([0-9]+).*Source=(.*/pe-[^-]+-(%%)[.]bz2).: (Stopped|Complete|Terminated)",
]

# vim:ts=4:sw=4:et:
