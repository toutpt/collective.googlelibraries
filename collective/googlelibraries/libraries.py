from zope import component
from zope import interface
from zope import schema
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from collective.googlelibraries import config
from collective.googlelibraries import interfaces
from collective.googlelibraries import messageFactory as _

class Library(object):
    interface.implements(interfaces.ILibrary)
    def __init__(self, id, title, version, url_u, url):
        self.id = id
        self.title = title
        self.version = version
        self._url_u = url_u
        self._url = url
        self.mode = 'minified'

    @property
    def url(self):
        if self.mode != 'minified':
            return self._url_u
        return self._url

#Now lets define all available libraries

GOOGLE_LIBRARIES = {}

GOOGLE_LIBRARIES["chrome-frame"] = {}
for v in ('1.0.0', '1.0.1', '1.0.2'):
    url = "https://ajax.googleapis.com/ajax/libs/chrome-frame/%s/CFInstall.min.js"%v
    url_u = "https://ajax.googleapis.com/ajax/libs/chrome-frame/%s/CFInstall.js"%v
    GOOGLE_LIBRARIES["chrome-frame"][v] = Library("chrome-frame","Chrome Frame", v, url_u, url)

GOOGLE_LIBRARIES["dojo"] = {}
for v in ('1.1.1',
          '1.2.0', '1.2.3',
          '1.3.0', '1.3.1', '1.3.2',
          '1.4.0', '1.4.1', '1.4.3',
          '1.5'):
    url_u = "https://ajax.googleapis.com/ajax/libs/dojo/%s/dojo/dojo.xd.js.uncompressed.js"%v
    url = "https://ajax.googleapis.com/ajax/libs/dojo/%s/dojo/dojo.xd.js"%v
    GOOGLE_LIBRARIES["dojo"][v] = Library("dojo","Dojo", v, url_u, url)

GOOGLE_LIBRARIES["ext-core"] = {}
for v in ('3.0.0','3.1.0'):
    url_u = "https://ajax.googleapis.com/ajax/libs/ext-core/%s/ext-core-debug.js"%v
    url = "https://ajax.googleapis.com/ajax/libs/ext-core/%s/ext-core.js"%v
    GOOGLE_LIBRARIES["ext-core"][v] = Library("ext-core","Ext Core", v, url_u, url)

GOOGLE_LIBRARIES["jquery"] = {}
for v in ('1.2.3', '1.2.6',
          '1.3.0', '1.3.1', '1.3.2',
          '1.4.0', '1.4.1', '1.4.2','1.4.3','1.4.4'):
    url_u = "https://ajax.googleapis.com/ajax/libs/jquery/%s/jquery.js"%v
    url = "https://ajax.googleapis.com/ajax/libs/jquery/%s/jquery.min.js"%v
    GOOGLE_LIBRARIES["jquery"][v] = Library("jquery","jQuery", v, url_u, url)

GOOGLE_LIBRARIES["jqueryui"] = {}
for v in ('1.5.2', '1.5.3',
          '1.6.0',
          '1.7.0','1.7.1', '1.7.2', '1.7.3',
          '1.8.0', '1.8.1', '1.8.2', '1.8.4', '1.8.5','1.8.6'):
    url_u = "https://ajax.googleapis.com/ajax/libs/jqueryui/%s/jquery-ui.js"%v
    url = "https://ajax.googleapis.com/ajax/libs/jqueryui/%s/jquery-ui.min.js"%v
    GOOGLE_LIBRARIES["jqueryui"][v] = Library("jqueryui","jQuery UI", v, url_u, url)

GOOGLE_LIBRARIES["mootools"] = {}
for v in ('1.1.1', '1.1.2', '1.2.1', '1.2.2', '1.2.3', '1.2.4', '1.2.5','1.3.0'):
    url_u = "https://ajax.googleapis.com/ajax/libs/mootools/%s/mootools.js"%v
    url = "https://ajax.googleapis.com/ajax/libs/mootools/%s/mootools-yui-compressed.js"%v
    GOOGLE_LIBRARIES["mootools"][v] =  Library("mootools","MooTools", v, url_u, url)

GOOGLE_LIBRARIES["prototype"] = {}
for v in ('1.6.0.2', '1.6.0.3', '1.6.1.0','1.7.0.0'):
    url_u = "https://ajax.googleapis.com/ajax/libs/prototype/%s/prototype.js"%v
    url = "https://ajax.googleapis.com/ajax/libs/prototype/%s/prototype.js"%v
    GOOGLE_LIBRARIES["prototype"][v] = Library("prototype","Prototype", v, url_u, url)

GOOGLE_LIBRARIES["scriptaculous"] = {}
for v in ('1.8.1', '1.8.2','1.8.3'):
    url_u = "https://ajax.googleapis.com/ajax/libs/scriptaculous/%s/scriptaculous.js"%v
    url = "https://ajax.googleapis.com/ajax/libs/scriptaculous/%s/scriptaculous.js"%v
    GOOGLE_LIBRARIES["scriptaculous"][v] = Library("scriptaculous","script.aculo.us", v, url_u, url)

GOOGLE_LIBRARIES["swfobject"] = {}
for v in ('2.1','2.2'):
    url_u = "https://ajax.googleapis.com/ajax/libs/swfobject/%s/swfobject_src.js"%v
    url = "https://ajax.googleapis.com/ajax/libs/swfobject/%s/swfobject.js"%v
    GOOGLE_LIBRARIES["swfobject"][v] = Library("swfobject","SWFObject", v, url_u, url)

GOOGLE_LIBRARIES["yui"] = {}
for v in ('2.6.0', '2.7.0', '2.8.0r4', '2.8.1','2.8.2'):
    url_u = "https://ajax.googleapis.com/ajax/libs/yui/%s/build/yuiloader/yuiloader.js"%v
    url = "https://ajax.googleapis.com/ajax/libs/yui/%s/build/yuiloader/yuiloader-min.js"%v
    GOOGLE_LIBRARIES["yui"][v] = Library("yui","Yahoo! User Interface Library (YUI)", v, url_u, url)

DEFAULT_LOADER_MODE_CHOICES = schema.vocabulary.SimpleVocabulary((
    schema.vocabulary.SimpleTerm('loader','loader',_(u'google.load')),
    schema.vocabulary.SimpleTerm('scripttag','scripttag',_(u'script tags')),
    schema.vocabulary.SimpleTerm('autoload','autoload',_(u'One request (auto load)')),
))

terms = []
for l in GOOGLE_LIBRARIES.keys():
    terms.append(schema.vocabulary.SimpleTerm(l,l,l))

GOOGLE_LIBRARIES_VOCABULARY = schema.vocabulary.SimpleVocabulary(terms)



class LibraryManager(SchemaAdapterBase):
    """The library manager. manage CRUD on Library"""
    component.adapts(IPloneSiteRoot)
    interface.implements(interfaces.ILibraryManager)

    def __init__(self, context):
        self.context = context

    def get_loader_mode(self):
        return getattr(self.properties, config.PROPERTY_LOADER_MODE_FIELD, '')

    def set_loader_mode(self, value):
        self.properties._updateProperty(config.PROPERTY_LOADER_MODE_FIELD, value)

    loader_mode = property(get_loader_mode, set_loader_mode)

    def get_libraries(self):
        return getattr(self.properties, config.PROPERTY_LIBRARIES_FIELD, '')

    def set_libraries(self, value):
        self.properties._updateProperty(config.PROPERTY_LIBRARIES_FIELD, value)

    libraries = property(get_libraries, set_libraries)

    @property
    def properties(self):
        return getToolByName(self.context, 'portal_properties').google_properties

    @property
    def libraries_dict(self):
        res = {}

        for lib in self.libraries:
            value = lib.split('|')
            libname = value[0].strip()
            version = value[1].strip()
            res[libname] = GOOGLE_LIBRARIES[libname][version]
        
        return res
