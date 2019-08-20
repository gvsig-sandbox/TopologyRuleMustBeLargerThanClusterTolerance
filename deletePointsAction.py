# encoding: utf-8

import gvsig
from gvsig import geom
from gvsig.geom import *
from org.gvsig.fmap.geom import GeometryLocator
from org.gvsig.fmap.geom import GeometryManager
from org.gvsig.fmap.geom import GeometryUtils
from org.gvsig.topology.lib.spi import AbstractTopologyRuleAction
import sys

from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

#from addons.TopologyRuleMustBeLargerThanClusterTolerance.mustBeLargerThanClusterToleranceFactory import MustBeLargerThanClusterToleranceRuleFactory
#from mustBeLargerThanClusterToleranceFactory import MustBeLargerThanClusterToleranceRuleFactory
from org.gvsig.topology.lib.api import ExecuteTopologyRuleActionException

#from mustBeLargerThanClusterToleranceRuleFactory import MustBeLargerThanClusterToleranceRuleFactory

class DeletePointsAction(AbstractTopologyRuleAction):

  def __init__(self):
    AbstractTopologyRuleAction.__init__(
      self,
      "MustBeLargerThanClusterTolerance", #MustBeLargerThanClusterToleranceRuleFactory.NAME,
      "DeletePointsAction",
      "Delete Points Action",
      "This action modifies polygon and line features whose points collapse during the validation process bassed on the topology's tolerance. This action can be applied to one or more Must Be Larger Than Cluster Tolerance errors."
    )
  
  logger("1", LOGGER_INFO)
  def execute(self, rule, line, parameters):
    #TopologyRule rule, TopologyReportLine line, DynObject parameters
    try:

      dataSet = rule.getDataSet1()
      reference = line.getFeature1()
      feature = reference.getFeature()
      geometryToFix = feature.getDefaultGeometry()
      tolerance = float(line.getData())
      geoManager = GeometryLocator.getGeometryManager()
      geomType = geometryToFix.getGeometryType().getType()
      subtype = geometryToFix.getGeometryType().getSubType()
      fixedGeometry = geoManager.create(geomType, subtype)

      def geometryToModify(geometryToFix):
        for i in range(0, geometryToFix.getNumVertices()):
          vertex1 = geometryToFix.getVertex(i)
          point = createPoint(D2, vertex1.getX(), vertex1.getY())
          if tolerance != 0:
            vertex1Tolerance = point.buffer(tolerance)
          else:
            vertex1Tolerance = point
          for j in range(0, geometryToFix.getNumVertices()):
            vertex2 = geometryToFix.getVertex(j)
            otherPoint = createPoint(D2, vertex2.getX(), vertex2.getY())
            if i==j:
              print "i, j", i, j
              continue
            else:
              print "i, j", i, j
              if not vertex1Tolerance.intersects(otherPoint):
                print "The distance is larger than the tolerance"
                if geoxAux.getNumVertices()==0:
                  print "addVertexIni"
                  geoxAux.addVertex(geometryToFix.getVertex(i))
                else:
                  print "The fixedGeometry vertices number is different from 0"
                content = False
                for k in range(0, geoxAux.getNumVertices()):
                  vertex = geoxAux.getVertex(k)
                  if vertex2 == vertex:
                    content = True
                    print "Content is True"
                  else:
                    print "Content is False"
                if content == False:
                  print "if content == False"
                  if j>i:
                    geoxAux.addVertex(geometryToFix.getVertex(j))
                    break
                  else:
                    print "vertex not added"
                else:
                  if j<i:
                    print "The vertex is already contained in the fixedGeometry"
                  elif j==geometryToFix.getNumVertices()-1:
                    geoxAux.addVertex(geometryToFix.getVertex(j))
                  else:
                    break
              else:
                print "The distance is less than the tolerance"

        return geoxAux

      if (GeometryUtils.isSubtype(geom.MULTICURVE, geometryToFix.getGeometryType().getType()) or 
         GeometryUtils.isSubtype(geom.MULTISURFACE, geometryToFix.getGeometryType().getType())):
        for x in range(0, geometryToFix.getPrimitivesNumber()):
          geox = geometryToFix.getPrimitiveAt(x)
          geoManager = GeometryLocator.getGeometryManager()
          geomType = geox.getGeometryType().getType()
          subtype = geox.getGeometryType().getSubType()
          geoxAux = geoManager.create(geomType, subtype)
          geoxAux = geometryToModify(geox)
          fixedGeometry.addPrimitive(geoxAux)
      else:
        geoxAux = fixedGeometry
        fixedGeometry = geometryToModify(geometryToFix)

      feature = feature.getEditable()
      feature.set("GEOMETRY", fixedGeometry)
      dataSet.update(feature)

    except:
      ex = sys.exc_info()[1]
      print "Error", ex.__class__.__name__, str(ex)
      #throw new ExecuteTopologyRuleActionException(ex);
      #raise ExecuteTopologyRuleActionException(ex)

def main(*args):

    c = DeletePointsAction()
    pass
