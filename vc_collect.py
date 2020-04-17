import argparse
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl
from contextlib import contextmanager

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', action='store', required=True)
    parser.add_argument('--user', action='store', required=True)
    parser.add_argument('--password', action='store', required=True)
    parser.add_argument('properties', nargs='*')
    return parser.parse_args()

@contextmanager
def connect_vc(host, user, password):
    try:
        si = SmartConnectNoSSL(host=host,
                               user=user,
                               pwd=password)
        yield si
    finally:
        Disconnect(si)


def mk_filter_spec(obj_set, prop_set):
    fs = vmodl.query.PropertyCollector.FilterSpec()
    fs.objectSet = obj_set
    fs.propSet = prop_set
    return fs

def mk_obj_spec(view_ref, traversal_spec):
    os = vmodl.query.PropertyCollector.ObjectSpec()
    os.obj = view_ref
    os.skip = True
    os.selectSet = [traversal_spec]
    return os

def mk_traversal_spec(view_ref):
    ts = vmodl.query.PropertyCollector.TraversalSpec()
    ts.name = 'traverseEntries'
    ts.path = 'view'
    ts.skip = False
    ts.type = view_ref.__class__
    return ts

def mk_prop_spec(obj_type, path_set=None):
    ps = vmodl.query.PropertyCollector.PropertySpec()
    ps.type = obj_type
    if not path_set:
        ps.all = True
    ps.pathSet = path_set
    return ps

def mk_view_ref(si, obj_type):
    container = si.content.rootFolder
    view_ref = si.content.viewManager.CreateContainerView(
        container=container,
        type=obj_type,
        recursive=True)
    return view_ref
# TODO: destroy it


def parse_content(content):
    return {ps.name: ps.val for ps in content.propSet}


def vc_collect():
    args = parse_args()
    with connect_vc(args.address, args.user, args.password) as si:
        view_ref = mk_view_ref(si, [vim.VirtualMachine])
        
        traversal_spec = mk_traversal_spec(view_ref)
        obj_spec = mk_obj_spec(view_ref, traversal_spec)
        properties = args.properties
        prop_spec = mk_prop_spec(vim.VirtualMachine, properties)
        filter_spec = mk_filter_spec([obj_spec], [prop_spec])
        
        collector = si.content.propertyCollector
        props = collector.RetrieveProperties([filter_spec])

        pprops = map(parse_content, props)
        print(list(pprops))
